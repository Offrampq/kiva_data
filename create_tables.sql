# create temporary today's id list
create table today_list 
	(id int, 
	primary key(id));



# daily update table
create table daily_update
	(id int,
	datetime varchar(400),
	togo varchar(400));



# basic info 1
create table basic_info1
	(funded_amount int,
	purpose varchar(400),
	posted_date varchar(400),
	sector varchar(400),
	borrower_count int,
	bonus_credit_eligibility boolean,
	loan_amount int,
	country varchar(400),
	longlat varchar(400),
	planned_expiration_date varchar(400),
	activity varchar(400),
	partner_id int,
	id int,
	primary key(id));


# basic info 2
create table basic_info2
	(gender_m int,
	term int,
	child_flag int,
	due_dil_type varchar(400),
	p_rating float,
	p_time_on_kiva int,
	p_borrowers int,
	p_total_loans varchar(400),
	interest_charged varchar(400),
	avg_cost_borrower varchar(400),
	profitablity float,
	loan_ppc float,
	deliquency float,
	risk_rate float,
	default_rate float,
	loss_rate float,
	id int,
	primary key(id));







