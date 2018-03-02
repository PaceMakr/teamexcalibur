from datetime import timedelta

from django.db import models
from django.utils import timezone
# Create your models here.
class Inventory(models.Model):
	company_id = models.IntegerField(default=1)
	product = models.CharField(max_length=200)
	stock = models.IntegerField(default=1)
	perish_datetime = models.DateTimeField(null=True, blank=True)
	datetime_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return '\t'.join(self.get_fields())
		'''date_added = self.datetime_added.date().strftime('%m/%d/%y')
		if self.perish_datetime:
			perish_date = self.perish_datetime.date().strftime('%m/%d/%y')
			return f'On {date_added} Company {self.company_id} added {self.stock} units of {self.product} which expire on {perish_date}'
		return f'On {date_added} Company {self.company_id} added {self.stock} units of {self.product}'
		'''
	def get_fields(self):
		return list(map(str, (self.company_id, self.product, self.stock, self.perish_datetime, self.datetime_added)))

class Log(models.Model):
	company_id = models.IntegerField(default=1)
	product_id = models.IntegerField(default=1)
	consumer = models.CharField(max_length=200)
	product = models.CharField(max_length=200)
	consumed = models.IntegerField(default=1)
	datetime_consumed = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.product} = {self.consumed} by {self.consumer}'

	def is_for_daily_report(self):
		return self.datetime_added >= timezone.now() - timedelta(1)

	def is_for_weekly_report(self):
		return self.datetime_added >= timezone.now() - timedelta(7)

