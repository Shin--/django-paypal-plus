# Generated by Django 2.2.28 on 2022-05-03 10:27

from django.db import migrations, models


def migrate_resource_state(apps, schema_editor):
    import json
    PaypalPayment = apps.get_model('django_paypal', 'PaypalPayment')

    for payment in PaypalPayment.objects.all():
        if payment.update_response_object:
            payment_response = json.loads(payment.update_response_object)
            if payment_response['state'] == 'approved':
                for transaction in payment_response['transactions']:
                    if 'related_resources' in transaction:
                        for resource in transaction['related_resources']:
                            if 'sale' in resource:
                                if 'state' in resource['sale']:
                                    payment.related_resource_state = resource['sale']['state']
                                    payment.save(update_fields=['related_resource_state'])


class Migration(migrations.Migration):

    dependencies = [
        ('django_paypal', '0003_auto_20200124_1528'),
    ]

    operations = [
        migrations.AddField(
            model_name='paypalpayment',
            name='related_resource_state',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='related resource state'),
        ),
        migrations.RunPython(migrate_resource_state, reverse_code=migrations.RunPython.noop, elidable=True)
    ]