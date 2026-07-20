import smtplib
from email.mime.text import MIMEText
import logging

def send_email(result: list[dict], config: dict) -> bool:
    try:
        email_from = config["email"]["from"]
        email_to = config["email"]["to"]
        password = config["email"]["password"]
        limit = config["email"]["limit"]
    
        text = ""

        for tender in result[:limit]:
            text += f"{tender['Название']}\n"
            text += f"Сумма: {tender['Сума']}\n"
            text += f"Ссылка: {tender['Ссылка']}\n\n"
            text += "--------------------\n"
            
        msg = MIMEText(text)
        msg["From"] = email_from
        msg["To"] = email_to
        msg["Subject"] = "Тендеры за сегодня:"

        logging.info("Подключение к SMTP...")
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=15) as server:
            server.starttls()
            logging.info("Отправка письма...")
            server.login(email_from, password)
            server.sendmail(email_from, email_to, msg.as_string())
        logging.info("Письмо отправлено")
        return True
    except (smtplib.SMTPException, OSError) as e:
        logging.error(f"Ошибка отправки: {e}")
        return False
