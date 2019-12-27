from datetime import datetime

from pyfastocloud_models.subscriber.entry import Subscriber
from pyfastocloud_models.subscriber.entry import Device
from app.service.service import ServiceSettings


def import_subscribers_to_server(db, server: ServiceSettings):
    cursor = db.cursor(dictionary=True)
    sql = 'SELECT username,password,created_at,exp_date FROM users'
    cursor.execute(sql)
    sql_subscribers = cursor.fetchall()

    for sql_entry in sql_subscribers:
        new_user = Subscriber.make_subscriber(email=sql_entry['username'], first_name=sql_entry['username'],
                                                  last_name=sql_entry['username'], password=sql_entry['password'],
                                                  country='US', language='US')
        new_user.status = Subscriber.Status.ACTIVE
        created_at = sql_entry['created_at']
        if created_at:
            new_user.created_date = datetime.fromtimestamp(created_at)
        exp_date = sql_entry['exp_date']
        if exp_date:
            new_user.exp_date = datetime.fromtimestamp(exp_date)
        dev = Device(name='Xtream')
        new_user.add_device(dev)
        # save
        new_user.add_server(server)
        server.add_subscriber(new_user)

    cursor.close()
