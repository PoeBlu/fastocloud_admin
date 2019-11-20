from app.home.entry import ProviderUser
from app.service.service import ServiceSettings, ProviderPair


def import_resellers_to_server(db, server: ServiceSettings):
    cursor = db.cursor(dictionary=True)
    sql = 'SELECT username,email,password from reg_users'
    cursor.execute(sql)
    sql_providers = cursor.fetchall()

    for sql_entry in sql_providers:
        email = sql_entry['email']
        password = sql_entry['email']
        new_user = ProviderUser.make_provider(email=email, password=password, country='US', language='en')
        new_user.status = ProviderUser.Status.ACTIVE
        new_user.save()

        admin = ProviderPair(new_user.id, ProviderPair.Roles.ADMIN)
        server.add_provider(admin)
        new_user.add_server(server)

    cursor.close()
