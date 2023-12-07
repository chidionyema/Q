from flask import logging
from flask_mail import Mail, Message
from app.engine import Pipeline2, OptimizerFactory, ModelBuilder, MappingLayer
from datetime import datetime
from app import create_app, db, celery, mail, socketio
from app.dbdata import TaskResult

def convert_to_date_only(datetime_obj):
    if isinstance(datetime_obj, datetime):
        return datetime_obj.strftime("%Y-%m-%d")
    elif isinstance(datetime_obj, str):
        dt_obj = datetime.strptime(datetime_obj, "%Y-%m-%dT%H:%M:%S.%fZ")
        return dt_obj.strftime("%Y-%m-%d")
    else:
        raise TypeError("Unsupported type for datetime conversion")

@celery.task
def send_activation_email(email, activation_link):
    with create_app().app_context():
        msg = Message('Account Activation', recipients=[email])
        msg.body = f'Click the following link to activate your account: {activation_link}'
        mail.send(msg)

@celery.task
def send_password_reset_email(email, reset_link):
    with create_app().app_context():
        msg = Message('Password Reset', recipients=[email])
        msg.body = f'Click the following link to reset your password: {reset_link}'
        mail.send(msg)


@celery.task(name='app.train_model_task', bind=True)
def train_model_task(self, configurations):
    with create_app().app_context():
        try:
            all_mae_values = []

            for config in configurations:
                # Parsing dates from string to datetime
                symbol = config['symbol']
                start_date = datetime.strptime(config['start_date'], "%Y-%m-%dT%H:%M:%S.%fZ")
                end_date = datetime.strptime(config['end_date'], "%Y-%m-%dT%H:%M:%S.%fZ")

                # Convert dates to string in the required format
                start_date_str = convert_to_date_only(start_date)
                end_date_str = convert_to_date_only(end_date)

                # Fetching model and optimizer classes
                model_class = MappingLayer.models_mapping.get(config['model_name'])
               # optimizer_class = MappingLayer.optimizers_mapping.get(config['optimizer_name'])
                optimizer = OptimizerFactory.create_optimizer(config['optimizer_name'], param_grid={"n_estimators": [10, 50, 100]})
                # optimizer = optimizer_class(param_grid={"n_estimators": [10, 50, 100]}) if optimizer_class else None

                # Setting up model builder and pipeline
                model_builder = ModelBuilder(model_class, optimizer=optimizer)
                stocks_info = [(symbol, start_date_str, end_date_str, 14, 3, model_builder)]
                pipeline = Pipeline2(stocks_info)
                predictions = pipeline.process_data_pipeline()

                # Collecting and appending results
                for prediction in predictions:
                    si, test_predictions, mae_val, mae_test = prediction
                    all_mae_values.append({'symbol': symbol, 'mae_val': mae_val, 'mae_test': mae_test})

            # Storing results in the database
            result = TaskResult(task_id=self.request.id, result=all_mae_values)
            db.session.add(result)
            db.session.commit()

            # Emitting socket message upon completion
            socketio.emit('training_complete', {'progress': 100, 'message': 'Training completed!', 'predictions': all_mae_values})

            return all_mae_values

        except Exception as e:
            db.session.rollback()
            raise e

def convert_to_date_only(datetime_obj):
    """Converts datetime object to date string."""
    return datetime_obj.strftime("%Y-%m-%d")
