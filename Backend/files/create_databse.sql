/*
create database IoT_db
use Iot_db
*/

create table Users(
	ID int identity(1,1) primary key NOT NULL,
	Email nvarchar(max) NOT NULL,
	Pwd nvarchar(max) NOT NULL,
	Nickname nvarchar(max) NOT NULL,
	Jwt_refresh nvarchar(max),
	FCM_token nvarchar(max),
	Photo nvarchar(max)
);

create table Cars(
	ID int identity(1,1) primary key NOT NULL,
	Plate nvarchar(7) NOT NULL,
	Brand nvarchar(max),
	Color nvarchar(max),
	ID_User int foreign key references Users(ID) NOT NULL
);

/* Dati inseriti dal produttore*/
create table Sensors(
	/*UUID4*/
	ID nvarchar(36) primary key NOT NULL,
);

create table Gates(
	ID nvarchar(36) foreign key references Sensors(ID) NOT NULL,
	ID_User int foreign key references Users(ID) NOT NULL,
	Name nvarchar(max) NOT NULL,
	Location nvarchar(max) NOT NULL,
	Latitude numeric(9,6) NOT NULL,
	Longitude numeric(9,6) NOT NULL,
	Photo nvarchar(max)
	CONSTRAINT PK_Gate primary key(ID, ID_User)
);

create table Users_Location(
	ID int foreign key references Users(ID) NOT NULL,
	Date_Time datetime DEFAULT current_timestamp NOT NULL,
	Latitude numeric(9,6) NOT NULL,
	Longitude numeric(9,6) NOT NULL,
);

create table Accesses(
	ID_User int foreign key references Users(ID) NOT NULL,
	ID_Gate nvarchar(36) foreign key references Sensors(ID) NOT NULL,
	ID_Car int foreign key references Cars(ID) NOT NULL,
	Date_Time datetime DEFAULT current_timestamp,
	Outcome nvarchar(10) NOT NULL CHECK (Outcome IN('Granted', 'Denied', 'Pending', 'Reported')),
	Photo nvarchar(max)
);

create table Guests(
	ID_Administrator int foreign key references Users(ID) NOT NULL,
	ID_Car int foreign key references Cars(ID) NOT NULL,
	Deadline datetime,
	Nickname nvarchar(max)
);

create table Guests_Accesses(
	ID_User int foreign key references Users(ID) NOT NULL,
	ID_Gate nvarchar(36) foreign key references Sensors(ID) NOT NULL,
	ID_Car int foreign key references Cars(ID) NOT NULL,
	Date_Time datetime DEFAULT current_timestamp,
	Outcome nvarchar(10) NOT NULL CHECK (Outcome IN('Granted', 'Denied', 'Pending', 'Reported')),
	Photo nvarchar(max)
);