from flask_mail import Mail, Message
from app.engine import Pipeline2, RandomForest, DataLoader, ModelBuilder, GridSearchOptimizer, RandomForestRegressor, MappingLayer
from datetime import datetime
from app import create_app, db, celery, mail, socketio
from dbdata import TaskResult

def convert_to_date_only(datetime_str):
    dt_obj = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    return dt_obj.strftime("%Y-%m-%d")

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


@celery.task(bind=True)
def train_model_task(self, configurations):
    with create_app().app_context():
        try:
            all_mae_values = []

            for config in configurations:
                symbol = config['symbol']
                start_date = datetime.strptime(config['start_date'], "%Y-%m-%dT%H:%M:%S.%fZ")
                end_date = datetime.strptime(config['end_date'], "%Y-%m-%dT%H:%M:%S.%fZ")

                # Convert start and end dates
                start_date = convert_to_date_only(start_date)
                end_date = convert_to_date_only(end_date)

                # Load model and optimizer classes from mappings
                model_class = MappingLayer.models_mapping.get(config['model_name'])
                optimizer_class = MappingLayer.optimizers_mapping.get(config['optimizer_name'])
                optimizer = optimizer_class(param_grid={"n_estimators": [10, 50, 100]}) if optimizer_class else None

                # Build and train the model
                model_builder = ModelBuilder(model_class, optimizer=optimizer)
                stocks_info = [(symbol, start_date, end_date, 14, 3, model_builder)]
                pipeline = Pipeline2(stocks_info)
                predictions = pipeline.process_data_pipeline()

                # Collect results
                for prediction in predictions:
                    si, test_predictions, mae_val, mae_test = prediction
                    all_mae_values.append({'symbol': symbol, 'mae_val': mae_val, 'mae_test': mae_test})

            # Store the result for all configurations
            result = TaskResult(task_id=self.request.id, result=all_mae_values)
            db.session.add(result)
            db.session.commit()

            # Notify completion
            socketio.emit('training_complete', {
                'progress': 100,
                'message': 'Training completed!',
                'predictions': all_mae_values
            })

            return all_mae_values

        except Exception as e:
            db.session.rollback()
            socketio.start_background_task(background_emit, 'training_error', {'error': str(e)})
            raise e

