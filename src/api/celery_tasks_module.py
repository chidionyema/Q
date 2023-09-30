
from celery_config import celery
from flask_mail import Mail, Message
from engine import Pipeline2, RandomForest, DataLoader


@celery.task
def send_activation_email(email, activation_link):
    msg = Message('Account Activation', recipients=[email])
    msg.body = f'Click the following link to activate your account: {activation_link}'
    mail.send(msg)


@celery.task
def send_password_reset_email(email, reset_link):
    msg = Message('Password Reset', recipients=[email])
    msg.body = f'Click the following link to reset your password: {reset_link}'
    mail.send(msg)

  # Make sure that on the frontend/client side, you are listening for these events (training_progress, training_complete, and training_error) to handle the emitted data accordingly.

@celery.task(bind=True)
def train_model_task(self, symbol, start_date, end_date, model):
    try:
        # Validate date format
        datetime.strptime(start_date, "%Y-%m-%d")
        datetime.strptime(end_date, "%Y-%m-%d")

        # Ensure the symbol is valid (add more validation if needed)
        if not symbol_is_valid(symbol):
            raise ValueError("Invalid symbol")

        # Your training code starts here
        rf_builder = ModelBuilder(RandomForestRegressor, optimizer=GridSearchOptimizer(param_grid={"n_estimators": [10, 50, 100]}))
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

        # Updating the task progress to 100% upon completion
        self.update_state(state='PROGRESS', meta={'progress': 100})
          # Done
         # Emit the predictions
        socketio.emit('training_complete', {'progress': 100, 'message': 'Training completed!', 'predictions': mae_values}, namespace='/training')

        return mae_values

    except Exception as e:
        socketio.emit('training_error', {'error': str(e)}, namespace='/training')
        raise e


       