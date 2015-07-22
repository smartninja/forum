# coding=utf-8
from google.appengine.api import mail

def email_new_topic(first_name, topic_name, topic_id, email):
    message_body = '''
    Živjo {0}!
    Na SmartNinja forumu se je odprla nova tema z imenom {1}.
    Pregledaš in komentiraš jo lahko tukaj: http://forum.smartninja.org/topic/{2}
    Lep pozdrav,
    SmartNinja Team
    '''.format(first_name.encode('utf-8'),
               topic_name.encode('utf-8'),
               str(topic_id).encode('utf-8'))

    html_message_body = '''
    <p>Živjo {0}!</p>
    <br>
    <p>Na SmartNinja forumu se je odprla nova tema z imenom {1}.</p>
    <p>Pregledaš in komentiraš jo lahko <strong><a href='http://forum.smartninja.org/topic/{2}'>tukaj</a></strong>.</p>

    <br>
    Lep pozdrav,
    SmartNinja Team
    '''.format(first_name.encode('utf-8'),
               topic_name.encode('utf-8'),
               str(topic_id).encode('utf-8'))

    message = mail.EmailMessage(sender="SmartNinja <info@smartninja.org>",
                                to="%s" % email,
                                subject="Nova objava na SmartNinja forumu",
                                reply_to="info@smartninja.org",
                                body=message_body,
                                html=html_message_body)
    message.send()


def email_new_comment(first_name, topic_name, topic_id, email):
    if first_name:
        message_body = '''
        Živjo {0}!

        Obveščamo te, da je bil na temi {1} objavljen nov komentar!
        Pregledaš in komentiraš lahko tukaj: http://forum.smartninja.org/topic/{2}


        Lep pozdrav,
        SmartNinja Team
        '''.format(first_name.encode('utf-8'),
                   topic_name.encode('utf-8'),
                   topic_id.encode('utf-8'))

        html_message_body = '''
        <p>Živjo {0}!</p>
        <p>Obveščamo te, da je bil na temi {1} objavljen nov komentar!</p>
        <p>Pregledaš in komentiraš lahko tukaj: http://forum.smartninja.org/topic/{2}</p>

        <br>
        Lep pozdrav,
        SmartNinja Team
        '''.format(first_name.encode('utf-8'),
                   topic_name.encode('utf-8'),
                   str(topic_id).encode('utf-8'))

    else:
        message_body = '''
        Živjo!

        Obveščamo te, da je bil na temi {0} objavljen nov komentar!
        Pregledaš in komentiraš lahko tukaj: http://forum.smartninja.org/topic/{1}


        Lep pozdrav,
        SmartNinja Team
        '''.format(topic_name.encode('utf-8'),
                   topic_id.encode('utf-8'))

        html_message_body = '''
        <p>Živjo!</p>
        <p>Obveščamo te, da je bil na temi {0} objavljen nov komentar!</p>
        <p>Pregledaš in komentiraš lahko tukaj: http://forum.smartninja.org/topic/{1}</p>

        <br>
        Lep pozdrav,
        SmartNinja Team
        '''.format(topic_name.encode('utf-8'),
                   str(topic_id).encode('utf-8'))

    message = mail.EmailMessage(sender="SmartNinja <info@smartninja.org>",
                                to="%s" % email,
                                subject="Nov komentar na SmartNinja forumu",
                                reply_to="info@smartninja.org",
                                body=message_body,
                                html=html_message_body)
    message.send()