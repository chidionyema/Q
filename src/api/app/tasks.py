from flask_mail import Mail, Message
from app.engine import Pipeline2, RandomForest, DataLoader, ModelBuilder, GridSearchOptimizer, RandomForestRegressor
from datetime import datetime
from app import create_app, db, celery, mail, socketio
from app.dbdata import TaskResult

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
def train_model_task(self, symbol, start_date, end_date, model):
    with create_app().app_context():
        try:
            # Validate date format
            datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%fZ")
            datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S.%fZ")

            start_date = convert_to_date_only(start_date)
            end_date = convert_to_date_only(end_date)

            # Training code
            rf_builder = ModelBuilder(RandomForest, optimizer=GridSearchOptimizer(param_grid={"n_estimators": [10, 50, 100]}))
            stocks_info = [(symbol, start_date, end_date, 14, 3, rf_builder)]
            pipeline = Pipeline2(stocks_info)
            predictions = pipeline.process_data_pipeline()

            mae_values = []
            for prediction in predictions:
                si, test_predictions, mae_val, mae_test = prediction
                mae_values.append({'mae_val': mae_val, 'mae_test': mae_test})

            # Store the result
            result = TaskResult(task_id=self.request.id, result=mae_values)
            db.session.add(result)
            db.session.commit()

            socketio.emit('training_complete', {
                'progress': 100,
                'message': 'Training completed!',
                'predictions': mae_values
            })

            return mae_values

        except Exception as e:
            db.session.rollback()
            
            # Emit error in a background task
            socketio.start_background_task(background_emit, 'training_error', {'error': str(e)})
            
            raise e

