# -*- coding: utf-8 -*-
from django.shortcuts import render, RequestContext
from django.shortcuts import render_to_response, HttpResponse
from django.http import HttpResponseRedirect
from travel.models import User, Account, Place, Willgo, Team
from django.core.files.base import ContentFile 
import time 
from time import strptime      
import datetime
import os

 # def getImg(request):

        # file_content = ContentFile(request.FILES['img'].read())  
        # img = ImageStore(name = request.FILES['img'].name, img =
 # request.FILES['img'])  
     # img.save()
import random
# Create your views here.


def login(request):
	error = []
	if request.method == 'POST':
		account = request.POST['Account']
		key = request.POST['Key']
		existed_account = Account.objects.filter(EmailAddress=account)
		key_right_account = Account.objects.filter(EmailAddress=account, Key=key)
		if not existed_account or not account or not key or '@' not in account:
			if '@' not in account:
				error.append('账号格式不合法')
			elif not existed_account:
				error.append('数据库中没有该ID')
			if not account:
				error.append('没有填写ID')
			if not key:
				error.append('没有填写密码')
			return render(request, 'login.html', {'Error': error}, context_instance = RequestContext(request))
		elif not key_right_account:
			error.append('密码错误')
			return render(request, 'login.html', {'Error': error}, context_instance = RequestContext(request))
		else:
			#acc = account.split('@')
			return HttpResponseRedirect('/' + account + '/main')
	return render(request, 'login.html', {'Error': error}, context_instance = RequestContext(request))

def newaccount(request):
	error = []
	if request.method == 'POST':
		account = request.POST['Account']
		key = request.POST['Key']
		key_affirm = request.POST['Key_affirm']
		existed_account = Account.objects.filter(EmailAddress=account)
		if existed_account or not account or not key or ('@' not in account) or (key != key_affirm):
			if '@' not in account:
				error.append('账号格式不合法')
			elif existed_account:
				error.append('数据库中已有该ID')
			if not key:
				error.append('没有填写密码')
			elif key != key_affirm:
				error.append('两次输入密码不匹配')
			return render(request, 'newaccount.html', {'Error': error}, context_instance = RequestContext(request))
		else:
			new_account = Account(EmailAddress=account, Key=key)
			new_account.save()
			return HttpResponseRedirect('/')
	return render(request, 'newaccount.html', {'Error': error}, context_instance = RequestContext(request))


def mainpage(request, emailaddress):
	place = []
	comment = []
	temp_tcomment = []
	tcomment = []
	i = 1
	re = Place.objects.filter(Order=0)
	length = len(re)
	for i in range(length):
		comment.append(re[i].Comment)
	for i in comment:
		if len(i) > 30:
			temp_tcomment.append(i)
	if 3 < length:
		min = 3
	else:
		min = length
	while len(temp_tcomment) < min and len(temp_tcomment) < 3:
		rand = random.randint(0, length - 1)
		temp_tcomment.append(comment[rand])
	
	while len(temp_tcomment) > 0:
		r = random.randint(0, len(temp_tcomment) - 1)
		tcomment.append(temp_tcomment[r])
		del(temp_tcomment[r])
	
	if len(tcomment) == 0:
		tcomment1 = '暂无评论'
		tcomment2 = '暂无评论'
		tcomment3 = '暂无评论'
	elif len(tcomment) == 1:
		tcomment1 = tcomment[0]
		tcomment2 = '暂无评论'
		tcomment3 = '暂无评论'
		
	elif len(tcomment) == 2:
		tcomment1 = tcomment[0]
		tcomment2 = tcomment[1]
		tcomment3 = '暂无评论'
	else:
		tcomment1 = tcomment[0]
		tcomment2 = tcomment[1]
		tcomment3 = tcomment[2]
		
	place1 = ''
	place2 = ''
	place3 = ''
	name1 = ''
	name2 = ''
	name3 = ''
	if Place.objects.filter(Comment=tcomment1):
		place1 = Place.objects.filter(Comment=tcomment1)[0]
		name1 = User.objects.filter(EmailAddress=place1.EmailAddress)[0]
	if Place.objects.filter(Comment=tcomment2):
		place2 = Place.objects.filter(Comment=tcomment2)[0]
		name2 = User.objects.filter(EmailAddress=place2.EmailAddress)[0]
	if Place.objects.filter(Comment=tcomment3):
		place3 = Place.objects.filter(Comment=tcomment3)[0]
		name3 = User.objects.filter(EmailAddress=place3.EmailAddress)[0]
	city_dict = ["北京", '哈尔滨', '银川', '长春', '沈阳', '天津', '石家庄', '济南', '杭州', '合肥', '福州', '澳门', '香港', '乌鲁木齐', '拉萨', '西宁', '贵州', '昆明', '西安', '兰州', '郑州', '太原', '广州', '桂林', '海口', '无锡', '华山', '黄山', '泰山', '九寨沟', '延安', '张家界', '长白山', '洛阳', '上海', '武汉', '南京']
	num = [0, 0, 0]
	view_city = []
	while len(view_city) < 8:
		rand = random.randint(1, 36)
		view_city.append(city_dict[rand])
	view_city1 = []
	view_city2 = []
	for i in range(4):
		view_city1.append(view_city[i])
	for i in range(4):
		view_city2.append(view_city[i+4])
		
	return render(request, 'mainpage.html', {'Emailaddress1':name1.EmailAddress, 'Emailaddress2':name2.EmailAddress, 'Emailaddress3':name3.EmailAddress, 'Name1':name1, 'Name2':name2, 'Name3':name3, 'Place1':place1, 'Place2':place2, 'Place3':place3, 'Comment1':tcomment1, 'Comment2':tcomment2, 'Comment3':tcomment3, 'Emailaddress':emailaddress, 'View1':view_city1, 'View2':view_city2}, context_instance = RequestContext(request))
	
def strtodatetime(datestr,format):       
	return datetime.datetime.strptime(datestr,format)
#----------------------------
def datediff(beginDate,endDate):   
	format="%Y-%m-%d";   
	bd=strtodatetime(beginDate,format)   
	ed=strtodatetime(endDate,format)       
	oneday=datetime.timedelta(days=1)   
	count=0 
	while bd!=ed:   
		ed=ed-oneday   
		count+=1 
	return count
	
def recommend(request, emailaddress):
	
	#TA的意向
	willgo = Willgo.objects.all()
	person = []
	
	date = []
	
	province = []
	city = []
	time0 = []
	low = []
	high = []
	count_var = 0
	index = []
	
	for i in willgo:
		index.append(count_var)
		person.append(i.EmailAddress)
		province.append(i.Province)
		city.append(i.City)
		time0.append(i.Time)
		low.append(i.Low)
		high.append(i.High)
		date.append(i.Date)
		count_var += 1

	#排序
	for i in index:
		t1 = strptime(str(date[i]), "%Y-%m-%d")
		
		for j in index:
			if j != i:
				t2 = strptime(str(date[j]), "%Y-%m-%d")
				if t1 < t2:
					temperson = person[i]
					temprovince = province[i]
					temcity = city[i]
					temtime = time0[i]
					temlow = low[i]
					temhigh = high[i]
					temdate = date[i]
					
					person[i] = person[j]
					province[i] = province[j]
					city[i] = city[j]
					time0[i] = time0[j]
					low[i] = low[j]
					high[i] = high[j]
					date[i] = date[j]
					
					person[j] = temperson
					province[j] =temprovince
					city[j] = temcity
					time0[j] = temtime
					low[j] = temlow
					high[j] = temhigh
					date[j] = temdate
	
	div_city = []
	temp = []
	record = []
	my_user = User.objects.filter(EmailAddress = emailaddress)
	if my_user:
		my_user = my_user[0]
	for i in index:
		if (i not in record) and person[i] == my_user:
			temp.append(i)
			record.append(i)
		else:
			continue
		for j in index:
			if j != i and city[i] == city[j] and (j not in record):
				if date[i] < date[j]:
					count = datediff(str(date[i]), str(date[j]))
					temp_value = time0[i]
				else:
					count = datediff(str(date[j]), str(date[i]))
					temp_value = time0[j]
				
				if temp_value > count:
					if low[i] > low[j] and high[i] > high[j] and low[i] < high[j]:
						if (float(high[j] - low[i]) / int(high[i] - low[i]) > 0.4) and \
						(float(high[j] - low[i]) / int(high[j] - low[j]) > 0.4):
							temp.append(j)
							record.append(j)
					elif low[i] > low[j] and high[i] <= high[j]:
						temp.append(j)
						record.append(j)
					elif low[i] <= low[j] and high[i] > high[j]:
						temp.append(j)
						record.append(j)
					elif low[i] <= low[j] and high[i] <= high[j] and low[j] < high[i]:
						if (float(high[i] - low[j]) / int(high[i] - low[i]) > 0.4) and \
						(float(high[i] - low[j]) / int(high[j] - low[j]) > 0.4):
							temp.append(j)
							record.append(j)
		if temp:
			div_city.append(temp)
		temp = []
		
		
	recommend_me = []
	for i in div_city:
		for j in i:
			if person[j] == my_user:
				recommend_me.append(i)
				break
	
	recommend_me_willgo = []
	for i in recommend_me:
		for j in i:
			if person[j] != my_user:
				will = Willgo.objects.filter(EmailAddress=person[j], Province=province[j], City=city[j], Time=time0[j])[0]
				recommend_me_willgo.append(will)
	# for i in date:
		# print i

	double = []
	for j in index:
		for k in index:
			if j != k:
				pass
				
	
	friends = []

	submit_willgo = []
	for element in willgo:
		if element.EmailAddress == my_user:
			continue
		else:
			submit_willgo.append(element)

	temp111 = []
	people = []
	dict = {}
	city_dict = ["北京", '哈尔滨', '银川', '长春', '沈阳', '天津', '石家庄', '济南', '杭州', '合肥', '福州', '澳门', '香港', '乌鲁木齐', '拉萨', '西宁', '贵州', '昆明', '西安', '兰州', '郑州', '太原', '广州', '桂林', '海口', '无锡', '华山', '黄山', '泰山', '九寨沟', '延安', '张家界', '长白山', '洛阳', '上海', '武汉', '南京']

	view_city = []
	while len(view_city) < 8:
		rand = random.randint(1, 36)
		view_city.append(city_dict[rand])
	view_city1 = []
	view_city2 = []
	for i in range(4):
		view_city1.append(view_city[i])
	for i in range(4):
		view_city2.append(view_city[i+4])
		willgo = Willgo.objects.all()
	
	
	submit = []
	#time.strftime('%Y-%m-%d',time.localtime(time.time()))
	if request.method == 'POST':
		submit = ['1']
		city = request.POST['city']
		province = request.POST['province']
		show_city = city
		show_province = province
		if city == '-1':
			show_city = '市'
			show_province = '选择省份'
		user = request.POST['user']
		date0 = request.POST['date0']
		date1 = request.POST['date1']
		cost0 = request.POST['cost0']
		cost1 =request.POST['cost1']
		
		submit_willgo1 = submit_willgo
		if city != '-1':
			submit_willgo1 = []
			for i in submit_willgo:
				if i.City == city:
					submit_willgo1.append(i)
			submit_willgo = submit_willgo1
		if user:
			submit_willgo = []
			for i in submit_willgo1:
				import sys 
				reload(sys) 
				sys.setdefaultencoding('utf8')
				if str(i.EmailAddress) == user:
					submit_willgo.append(i)
			# for k in submit_willgo:
				# print k.City
			submit_willgo1 = submit_willgo
		if date0 and date1:
			submit_willgo1 = []
			for i in submit_willgo:
				# time1 = '2015-10-08'
				# time2 = '2015-10-06'
				# t1 = strptime(time1, "%Y-%m-%d")
				# t2 = strptime(time2, "%Y-%m-%d")
				# print t1 < t2
				t0 = strptime(str(i.Date), "%Y-%m-%d")
				t1 = strptime(date0, "%Y-%m-%d")
				t2 = strptime(date1, "%Y-%m-%d")
				if t0 >= t1 and t0 <= t2:
					submit_willgo1.append(i)
			submit_willgo = submit_willgo1
			for k in submit_willgo:
				print k.City
		if cost0 and cost1:
			submit_willgo = []
			for i in submit_willgo1:
				if i.Low >= int(cost0) and i.High <= int(cost1):
					print "****"
					submit_willgo.append(i)
			submit_willgo1 = submit_willgo
		return render(request, 'recommend.html', {'submit':submit, 'show_date0':date0, 'show_date1':date1, 'show_cost0':cost0, 'show_cost1':cost1, 'show_user':user, 'show_province':show_province, 'show_city':show_city, 'recommend_me_willgo':recommend_me_willgo, 'willgo':submit_willgo, 'friends':temp111, 'Emailaddress':emailaddress, 'View1':view_city1, 'View2':view_city2}, context_instance = RequestContext(request))
	
	#更新意向的状态，如果过期或满员，则更新status字段
	#User.objects.filter(EmailAddress=emailaddress).update(Name=name)
	current_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
	current_time = strptime(str(current_time), '%Y-%m-%d')
	# date1 = strptime(str(date), '%Y-%m-%d')
	for x in submit_willgo:
		temp_date = strptime(str(x.Date), '%Y-%m-%d')
		temp_user = User.objects.filter(Name=x.EmailAddress)[0]
		temp_team = Team.objects.filter(Owner=temp_user.EmailAddress, City=x.City, Date=x.Date)[0]
		count = 0
		temp_mem = temp_team.Mem.all()
		for i in temp_mem:
			count += 1
		if temp_date < current_time:
			x.Status='已过期'
			x.save()
		elif count == 5:
			x.Status='成员已满'
			x.save()
		else:
			x.Status='等待加入'
			x.save()
	return render(request, 'recommend.html', {'recommend_me_willgo':recommend_me_willgo, 'willgo':submit_willgo, 'friends':temp111, 'Emailaddress':emailaddress, 'View1':view_city1, 'View2':view_city2}, context_instance = RequestContext(request))
def foot(request, emailaddress):
	submit = False
	placeview = Place.objects.filter(EmailAddress=emailaddress)
	fillinformation = []
	if request.method == 'POST':
		submitemailaddress = Account.objects.filter(EmailAddress=emailaddress)[0]
		place = request.POST['place']
		comment = request.POST['comment']
		newcomment = Place(EmailAddress=submitemailaddress, Place=place, Order=0, Comment=comment)
		newcomment.save()
		if not User.objects.filter(EmailAddress=emailaddress):
			fillinformation.append(0)
			return render(request, 'foot.html', {'Fillinformation':fillinformation}, context_instance = RequestContext(request))
		submit = True
		return HttpResponseRedirect('/' + emailaddress + '/' + place + '/photos')
	return render(request, 'foot.html', {'Fillinformation':fillinformation, 'Emailaddress':emailaddress, 'Submit':submit, 'Placeview':placeview}, context_instance = RequestContext(request))

def postway(request, strName):
	if not request.POST.has_key(strName):
		return "" 
	if request.POST[strName]:
		return ','.join(request.POST.getlist(strName)) 
	else:
		return ""
	
def fillinformation(request, emailaddress):
	submit = False

	user = User.objects.filter(EmailAddress=emailaddress)
	if user:
		user = User.objects.filter(EmailAddress=emailaddress)[0]

	male = False
	female = False
	
	tsilence = False
	tactive = False
	tchat = False
	tmisspast = False
	
	man = User.objects.filter(EmailAddress=emailaddress, Gender='man')
	silence = User.objects.filter(EmailAddress=emailaddress, Silence=True)
	if silence:
		tsilence = True
	active = User.objects.filter(EmailAddress=emailaddress, Active=True)
	if active:
		tactive = True
	chat = User.objects.filter(EmailAddress=emailaddress, Chat=True)
	if chat:
		tchat = True
	misspast = User.objects.filter(EmailAddress=emailaddress, MissPast=True)
	if misspast:
		tmisspast = True
	if not man:
		female = True
	elif man:
		male = True
	
	if request.method == 'POST':
		if not user:
			submitemailaddress = Account.objects.filter(EmailAddress=emailaddress)[0]
			name = request.POST['name']
			gender = request.POST['1']
			age = request.POST['age']
			email = request.POST['email']
			discription = request.POST['discription']
			character = postway(request, 'character')
			place = postway(request, 'place')
			ch = character.split(',')
			pl = place.split(',')
			silence = False
			active = False
			chat = False
			misspast = False
			submit = True
			if 'silence' in ch:
				silence = True
			if 'active' in ch:
				active = True
			if 'chat' in ch:
				chat = True
			if 'misspast' in ch:
				misspast = True

			newuser = User(EmailAddress=submitemailaddress, Name=name, Email = email, Gender=gender, Age=age, Silence=silence, Active=active, Chat=chat, MissPast=misspast, Discription=discription)
			newuser.save()
		else:
			submitemailaddress = Account.objects.filter(EmailAddress=emailaddress)[0]
			name = request.POST['name']
			User.objects.filter(EmailAddress=emailaddress).update(Name=name)
			gender = request.POST['1']
			User.objects.filter(EmailAddress=emailaddress).update(Gender=gender)
			age = request.POST['age']
			User.objects.filter(EmailAddress=emailaddress).update(Age=age)
			discription = request.POST['discription']
			User.objects.filter(EmailAddress=emailaddress).update(Discription=discription)
			email = request.POST['email']
			User.objects.filter(EmailAddress=emailaddress).update(Email=email)
			character = postway(request, 'character')
			place = postway(request, 'place')
			ch = character.split(',')
			pl = place.split(',')
			silence = False
			active = False
			chat = False
			misspast = False
			submit = True
			if 'silence' in ch:

				User.objects.filter(EmailAddress=emailaddress).update(Silence=True)
			else:
				User.objects.filter(EmailAddress=emailaddress).update(Silence=False)
			if 'active' in ch:

				User.objects.filter(EmailAddress=emailaddress).update(Active=True)
			else:
				User.objects.filter(EmailAddress=emailaddress).update(Active=False)
			if 'chat' in ch:

				User.objects.filter(EmailAddress=emailaddress).update(Chat=True)
			else:
				User.objects.filter(EmailAddress=emailaddress).update(Chat=False)
			if 'misspast' in ch:

				User.objects.filter(EmailAddress=emailaddress).update(MissPast=True)
			else:
				User.objects.filter(EmailAddress=emailaddress).update(MissPast=False)
		user = User.objects.filter(EmailAddress=emailaddress)[0]
		male = False
		female = False
		
		tsilence = False
		tactive = False
		tchat = False
		tmisspast = False
		
		man = User.objects.filter(EmailAddress=emailaddress, Gender='man')
		silence = User.objects.filter(EmailAddress=emailaddress, Silence=True)
		if silence:
			tsilence = True
		active = User.objects.filter(EmailAddress=emailaddress, Active=True)
		if active:
			tactive = True
		chat = User.objects.filter(EmailAddress=emailaddress, Chat=True)
		if chat:
			tchat = True
		misspast = User.objects.filter(EmailAddress=emailaddress, MissPast=True)
		if misspast:
			tmisspast = True
		if not man:
			female = True
		elif man:
			male = True
	return render(request, 'fillinformation.html', {'Emailaddress':emailaddress, 'Tsilence':tsilence, 'Tactive':tactive, 'Tchat':tchat, 'Tmisspast':tmisspast, 'Man':male, 'Woman':female, 'Submit':submit, 'User':user, 'Emailaddress':emailaddress}, context_instance = RequestContext(request))
	
def security(request, emailaddress):
	submit = False
	error = []
	if request.method == 'POST':
		old_p = request.POST['old_p']
		new_p1 = request.POST['new_p1']
		new_p2 = request.POST['new_p2']
		existed_account = Account.objects.filter(EmailAddress=emailaddress, Key = old_p)
		if not existed_account or not old_p or (new_p1 != new_p2) or not new_p1 or not new_p2:
			if not existed_account:
				error.append('原密码不正确')
			if not old_p:
				error.append('没有填写密码')
			elif new_p1 != new_p2:
				error.append('两次输入密码不匹配')
			if not new_p1:
				error.append('没有填写新密码')
			if not new_p2:
				error.append('没有确认新密码')
		else:
			existed_account[0].Key = new_p1
			existed_account[0].save()
			submit=True
			return render(request, 'security.html', {'Emailaddress':emailaddress, 'Error': error, 'Emailaddress':emailaddress, 'Submit':submit}, context_instance = RequestContext(request))
	return render(request, 'security.html', {'Emailaddress':emailaddress, 'Error': error, 'Emailaddress':emailaddress, 'Submit':submit}, context_instance = RequestContext(request))

	
def file_count(dirname,filter_types=[]):
	count=0
	filter_is_on=False
	if filter_types!=[]:
		filter_is_on=True
	for item in os.listdir(dirname):
		abs_item=os.path.join(dirname,item)
		if os.path.isdir(abs_item): 
			count+=file_count(abs_item,filter_types)
		elif os.path.isfile(abs_item):
			if filter_is_on:
				extname=os.path.splitext(abs_item)[1]
				if extname in filter_types:
					count+=1
			else:
				count+=1
	return count
def commentview(request, emailaddress, place):
	counter = file_count('C:/Users/Paul_Yu/myproject/static/images/' + emailaddress + '/' + place)
	#print counter
	count = []
	i = 1
	while i <= counter:
		count.append(str(i))
		i += 1
	re_place = Place.objects.filter(EmailAddress=emailaddress, Place=place)
	comment = re_place[0].Comment
	return render_to_response('commentview.html', {'Count':count, 'Emailaddress':emailaddress, 'Place': place, 'Comment':comment})
def information(request, name): #想去地方相同且姓名相同的情况有可能会出错
	user = User.objects.filter(Name=name)[0]
	character = []
	if User.objects.filter(Name=name, Silence=True):
		character.append('安静')
	if User.objects.filter(Name=name, Active=True):
		character.append('活泼')
	if User.objects.filter(Name=name, Chat=True):
		character.append('健谈')
	if User.objects.filter(Name=name, MissPast=True):
		character.append('怀旧')
	return render_to_response('information.html', {'User':user, 'Character':character})

def willgo(request, emailaddress):
	submit = False
	error = []
	if request.method == 'POST':
		from_place = request.POST['from']
		province = request.POST['province']
		city = request.POST['city']
		date = request.POST['date']
		time0 = request.POST['time']
		cost_low = request.POST['low']
		cost_high = request.POST['high']
		user = User.objects.filter(EmailAddress=emailaddress)[0]
		#print from_place, province, city, date, time0, cost_low, cost_high
		
		current_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
		current_time = strptime(str(current_time), '%Y-%m-%d')
		date1 = strptime(str(date), '%Y-%m-%d')
		if date1 < current_time:
			willgo = Willgo(EmailAddress=user, From=from_place, Province=province, City=city, Date=date, Time=time0, Low=cost_low, High=cost_high, Status = '已过期')
		else:
			willgo = Willgo(EmailAddress=user, From=from_place, Province=province, City=city, Date=date, Time=time0, Low=cost_low, High=cost_high, Status = '等待加入')
		willgo.save()
		owner = Account.objects.filter(EmailAddress=emailaddress)[0]
		team = Team(Owner=owner, Province=province, City=city, Date=date)
		team.save()
		team.Mem.add(User.objects.filter(Name=user)[0])
		team.save()
		# Team.objects.all().delete()
		submit = True
		return render(request, 'willgo.html', {'Emailaddress':emailaddress, 'Submit':submit}, context_instance = RequestContext(request))
	return render(request, 'willgo.html', {'Emailaddress':emailaddress, 'Error': error, 'Emailaddress':emailaddress, 'Submit':submit}, context_instance = RequestContext(request))
	
def myteam(request, emailaddress):
	submit = False
	error = []
	me = User.objects.filter(EmailAddress= emailaddress)
	if me:
		me = me[0]
	user = User.objects.filter(EmailAddress=emailaddress)
	if user:
		user = user[0]
	current_user = Willgo.objects.filter(EmailAddress=user)
	myteam = Team.objects.filter(Owner=emailaddress)

	joinedteam = []
	for i in Team.objects.all():
		if me in i.Mem.all():
			print me, "at", i
			if str(i.Owner) != emailaddress:
				joinedteam.append(i)

	willgo = Willgo.objects.all()
	submit_willgo =[]
	for element in willgo:
		for inside in joinedteam:
			if element.EmailAddress == User.objects.filter(EmailAddress=inside.Owner)[0]:
				if element.City == inside.City:
					submit_willgo.append(element)
					
	# current_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
	# current_time = strptime(str(current_time), '%Y-%m-%d')
	# for x in submit_willgo:
		# temp_date = strptime(str(x.Date), '%Y-%m-%d')
		# temp_user = User.objects.filter(Name=x.EmailAddress)[0]
		# temp_team = Team.objects.filter(Owner=temp_user.EmailAddress, City=x.City, Date=x.Date)[0]
		# count = 0
		# temp_mem = temp_team.Mem.all()
		# for i in temp_mem:
			# count += 1
		# if temp_date < current_time:
			# x.Status='已过期'
			# x.save()
		# elif count == 5:
			# x.Status='成员已满'
			# x.save()
	current_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
	current_time = strptime(str(current_time), '%Y-%m-%d')
	for x in current_user:
		temp_date = strptime(str(x.Date), '%Y-%m-%d')
		if temp_date < current_time:
			x.Status='已过期'
			x.save()
	for x in joinedteam:
		temp_date = strptime(str(x.Date), '%Y-%m-%d')
		if temp_date < current_time:
			x.Status='已过期'
			x.save()
	return render(request, 'myteam.html', {'user':current_user, 'joinedteam':submit_willgo, 'Emailaddress':emailaddress, 'Error': error, 'Emailaddress':emailaddress, 'Submit':submit}, context_instance = RequestContext(request))

def travel_details(request, user, city, joiner):
	error = []
	submit = False
	user = User.objects.filter(Name = user)[0]
	willgo = Willgo.objects.filter(EmailAddress=user, City=city)[0]
	travel_user = User.objects.filter(Name = user)[0]
	team = Team.objects.filter(City = city, Owner=travel_user.EmailAddress)[0]
	submit_team = team.Mem.all()
	print submit_team
	joined = []
	judge_joined = User.objects.filter(EmailAddress=joiner)[0]
	if judge_joined in submit_team:
		joined.append('1')
	if request.method == 'POST':
		submit = True
		
		if len(team.Mem.all()) < 5:
			join_user = User.objects.filter(EmailAddress=joiner)[0]
			team.Mem.add(join_user)
			joiner_team = Team.objects.filter(Owner=joiner, City=city)
			joiner_willgo = Willgo.objects.filter(EmailAddress=judge_joined, City=city)
			if joiner_team:
				joiner_team[0].delete()
			if joiner_willgo:
				joiner_willgo[0].delete()
		return HttpResponseRedirect('/'+str(joiner)+'/'+'recommend')
	return render(request, 'travel_details.html', {'joined':joined, 'team':submit_team, 'willgo':willgo, 'Error': error, 'Submit':submit}, context_instance = RequestContext(request))


def travel_delete(request, user, city, joiner):
	error = []
	submit = False
	user = User.objects.filter(Name = user)[0]
	willgo = Willgo.objects.filter(EmailAddress=user, City=city)[0]
	travel_user = User.objects.filter(Name = user)[0]
	team = Team.objects.filter(City = city, Owner=travel_user.EmailAddress)[0]
	submit_team = team.Mem.all()
	print submit_team
	judge_joined = User.objects.filter(EmailAddress=joiner)[0]
	if request.method == 'POST':
		submit = True
		joiner_team = Team.objects.filter(Owner=joiner, City=city)[0]
		joiner_willgo = Willgo.objects.filter(EmailAddress=judge_joined, City=city)[0]
		if joiner_team:
				joiner_team.delete()
		if joiner_willgo:
				joiner_willgo.delete()
		return HttpResponseRedirect('/'+str(joiner)+'/'+'myteam')
	return render(request, 'travel_delete.html', {'team':submit_team, 'willgo':willgo, 'Error': error, 'Submit':submit}, context_instance = RequestContext(request))
	
def travel_leave(request, user, city, joiner):
	error = []
	submit = False
	user = User.objects.filter(Name = user)[0]
	willgo = Willgo.objects.filter(EmailAddress=user, City=city)[0]
	travel_user = User.objects.filter(Name = user)[0]
	team = Team.objects.filter(City = city, Owner=travel_user.EmailAddress)[0]
	submit_team = team.Mem.all()
	#print submit_team

	if request.method == 'POST':
		judge_joined = User.objects.filter(EmailAddress=joiner)[0]
		submit = True
		for i in submit_team:
			print i, judge_joined, "**"
			if str(i) == str(judge_joined):
				team.Mem.remove(i) 
		#submit_team = temp
		return HttpResponseRedirect('/'+str(joiner)+'/'+'myteam')
	return render(request, 'travel_leave.html', {'team':submit_team, 'willgo':willgo, 'Error': error, 'Submit':submit}, context_instance = RequestContext(request))

from PIL import Image
def photos(request, emailaddress, place):
	submit = []
	count = '1'
	if request.method == 'POST':
		submit = ['1']
		cwd = os.getcwd() 
		#print(cwd)
		try:
			reqfile = request.FILES['picfile'] #picfile要和html里面一致
			img = Image.open(reqfile)
			img.thumbnail((500,500),Image.ANTIALIAS) #对图片进行等比缩放
			
			if os.path.exists(cwd + '/static/images/' + emailaddress + '/' + place):
				while os.path.exists(cwd + '/static/images/' + emailaddress + '/' + place + '/' + count + '.png'):
					count = str(int(count) + 1)
				img.save(cwd + '/static/images/' + emailaddress + '/' + place + '/' + count +'.png',"png") #保存图片
			else:
				os.makedirs(cwd + '/static/images/' + emailaddress +'/' + place)
				img.save(cwd + '/static/images/' + emailaddress + '/' + place + '/' + count +'.png',"png")
		except Exception,e:
			return HttpResponse("Error %s"%e)#异常，查看报错信息
	return render(request, 'index.html', {'Count':count, 'Submit':submit, 'Emailaddress':emailaddress, 'place':place}, context_instance = RequestContext(request))

def allcomments(request, emailaddress):
	place = Place.objects.all()
	return render(request, 'allcomments.html', {'Place':place}, context_instance = RequestContext(request))