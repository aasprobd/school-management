class NotificationService:
    @staticmethod
    def send_notification(user_email: str, message: str, method: str = "email"):
        # This is a mock gateway. In production, connect to Twilio/SendGrid/etc.
        print(f"[MOCK NOTIFICATION] Method: {method} | To: {user_email} | Message: {message}")
        return True

    @staticmethod
    def broadcast_event(event_title: str):
        print(f"[MOCK BROADCAST] Event: {event_title} is coming up!")
        return True
