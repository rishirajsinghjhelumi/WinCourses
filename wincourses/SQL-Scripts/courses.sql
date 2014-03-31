/* WinCourses Schema */


CREATE TABLE IF NOT EXISTS 
`institutes` (
	`id` int(11) AUTO_INCREMENT,
	`name` varchar(256),
	PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1; 



CREATE TABLE IF NOT EXISTS 
`faculty` (
	`id` int(11) AUTO_INCREMENT,
	`name` varchar(256),
	`email` varchar(256) NOT NULL,
	`institute_id` int(11),
	`title` varchar(256),
	FOREIGN KEY (`institute_id`) REFERENCES institutes(`id`),
	PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1; 



CREATE TABLE IF NOT EXISTS 
`students` (
	`id` int(11) AUTO_INCREMENT,
	`name` varchar(256),
	`email` varchar(256) NOT NULL,
	`institute_id` int(11),
	`institute_roll_num` varchar(64),
	`password` varchar(256),
	FOREIGN KEY (`institute_id`) REFERENCES institutes(`id`),
	PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1; 



CREATE TABLE IF NOT EXISTS 
`courses` (
	`id` int(11) AUTO_INCREMENT,
	`name` varchar(256),
	`code` varchar(64),
	`year` varchar(64),
	`description` varchar(4096),
	`institute_id` int(11),
	FOREIGN KEY (`institute_id`) REFERENCES institutes(`id`),
	PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



CREATE TABLE IF NOT EXISTS 
`course_students` (
	`id` int(11) AUTO_INCREMENT,
	`course_id` int(11),
	`student_id` int(11),
	FOREIGN KEY (`course_id`) REFERENCES courses(`id`),
	FOREIGN KEY (`student_id`) REFERENCES students(`id`),
	PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



CREATE TABLE IF NOT EXISTS 
`course_faculty` (
	`id` int(11) AUTO_INCREMENT,
	`course_id` int(11),
	`faculty_id` int(11),
	FOREIGN KEY (`course_id`) REFERENCES courses(`id`),
	FOREIGN KEY (`faculty_id`) REFERENCES faculty(`id`),
	PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



CREATE TABLE IF NOT EXISTS 
`attachments` (
	`id` int(11) AUTO_INCREMENT,
	`type` varchar(256),
	`location` varchar(2048),
	PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1; 



CREATE TABLE IF NOT EXISTS 
`course_resources` (
	`id` int(11) AUTO_INCREMENT,
	`course_id` int(11),
	`attachment_id` int(11),
	`description` varchar(4096),
	FOREIGN KEY (`course_id`) REFERENCES courses(`id`),
	FOREIGN KEY (`attachment_id`) REFERENCES attachments(`id`),
	PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



CREATE TABLE IF NOT EXISTS 
`course_assignments` (
	`id` int(11) AUTO_INCREMENT,
	`description` varchar(4096),
	`uploaded` varchar(256),
	`due_date` varchar(256),
	`is_active` boolean,
	`course_id` int(11),
	`attachment_id` int(11),
	FOREIGN KEY (`course_id`) REFERENCES courses(`id`),
	FOREIGN KEY (`attachment_id`) REFERENCES attachments(`id`),
	PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



CREATE TABLE IF NOT EXISTS 
`course_marks` (
	`id` int(11) AUTO_INCREMENT,
	`exam` varchar(256),
	`marks` int(11),
	`total_marks` int(11),
	`course_id` int(11),
	`student_id` int(11),
	FOREIGN KEY (`course_id`) REFERENCES courses(`id`),
	FOREIGN KEY (`student_id`) REFERENCES students(`id`),
	PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;




CREATE TABLE IF NOT EXISTS 
`questions` (
	`id` int(11) AUTO_INCREMENT,
	`question` varchar(4096),
	`option_a` varchar(256),
	`option_b` varchar(256),
	`option_c` varchar(256),
	`option_d` varchar(256),
	`correct_option` int(1),
	PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



CREATE TABLE IF NOT EXISTS 
`course_quiz` (
	`id` int(11) AUTO_INCREMENT,
	`course_id` int(11),
	`title` varchar(256),
	`duration` int(11),
	`is_active` boolean,
	FOREIGN KEY (`course_id`) REFERENCES courses(`id`),
	PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



CREATE TABLE IF NOT EXISTS 
`quiz_questions` (
	`id` int(11) AUTO_INCREMENT,
	`course_quiz_id` int(11),
	`question_id` int(11),
	FOREIGN KEY (`course_quiz_id`) REFERENCES course_quiz(`id`),
	FOREIGN KEY (`question_id`) REFERENCES questions(`id`),
	PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1; 



INSERT INTO `institutes` (`name`) VALUES 
	('IIIT Hyderabad'),
	('BITS PILANI, Hyderabad');


INSERT INTO `students` (`id`, `name`, `email`, `institute_id`, `institute_roll_num`, `password`) VALUES
	(1, 'a', 'a', 1, 'a', 'ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb');


INSERT INTO `courses`(`name`, `code`, `year` , `description`, `institute_id`) VALUES 
	('Computer Programming', 'CS101', '2014 - Spring', 'Computer Programming Course', 1), 
	('Science', 'SC101', '2014 - Spring', 'Science : Quantum Mechanics', 1), 
	('Computer Algorithms', 'CS102', '2014 - Spring', 'Algorithms and Computer Logic', 1), 
	('Algebra', 'MA101', '2014 - Spring', 'Introduction to Linear Algebra', 1),
	('ITWS', 'CS111', '2014 - Spring', 'HTML, CSS, ASP, Python', 1);


INSERT INTO `course_students`(`course_id`, `student_id`) VALUES 
	(3,1);

INSERT INTO `faculty`(`name`, `email`, `institute_id`, `title`) VALUES
	('Kannan', 'kannan@iiit.ac.in', 1, 'Prof'),
	('kaul', 'kaul@iiit.ac.in', 1, 'Prof'),
	('kishore', 'kishore@iiit.ac.in', 1, 'Asst. Prof'),
	('Vasudeva', 'Vasudeva@iiit.ac.in', 1, 'Dean');

INSERT INTO `course_faculty`(`course_id`, `faculty_id`) VALUES
	(1,1),
	(1,3),
	(2,1),
	(3,4),
	(3,2),
	(4,4),
	(4,1),
	(5,2);

INSERT INTO `attachments`(`type`, `location`) VALUES
	('url','http://www.cs.bu.edu/AboutCS/WhatIsCS.pdf'),
	('url','http://cs.brown.edu/about/brochure.pdf'),
	('url','http://t1.gstatic.com/images?q=tbn:ANd9GcRbLABkAGOTKN7b1pEg2doiOjwfPTDECVZziHFLcGdvk0XNsbJtoA'),
	('url','http://www.w3schools.com/tags/tag_input.asp'),
	('url','https://en.wikipedia.org/wiki/Text_types'),
	('url','http://www.ets.org/s/gre/pdf/gre_math_review.pdf');

INSERT INTO `course_resources`(`course_id`, `attachment_id`,`description`) VALUES
	(1,1,'What is CS?'),
	(1,2,'Brochure'),
	(1,4,'Tags'),
	(2,3,'Periodic Table'),
	(2,4,'Tags'),
	(3,1,'What is CS?'),
	(3,2,'Brochure'),
	(5,2,'Brochure'),
	(5,6,'Maths Review'),
	(4,6,'Maths Review'),
	(4,5,'Text Types'),
	(4,3,'Periodic Table');

INSERT INTO `course_assignments`(`course_id`, `attachment_id`, `description`, `uploaded`, `due_date`, `is_active`) VALUES
	(1,1,'Assignment on Logic', '2014-03-01', '2014-04-22', 0),
	(1,2,'Assignment on Array', '2014-03-28', '2014-04-05', 1),
	(2,3,'Assignment on Logic', '2014-03-28', '2014-04-05', 1),
	(3,5,'Assignment on Logic', '2014-03-28', '2014-04-05', 1),
	(4,4,'Assignment on Logic', '2014-03-28', '2014-04-05', 1),
	(5,1,'Assignment on Logic', '2014-03-28', '2014-04-05', 1);

INSERT INTO `course_marks`(`course_id`,`student_id`,`exam`, `marks`,`total_marks`) VALUES
	(1,1,'Class Quiz 1',8,10),
	(1,1,'Class Quiz 2',6,10),
	(1,1,'Assignment 1',80,100),
	(1,1,'MidSem 1',28,40),
	(2,1,'Class Quiz 1',8,10),
	(3,1,'Class Quiz 1',8,10),
	(4,1,'Class Quiz 1',8,10);

INSERT INTO `course_quiz`(`course_id`,`title`, `duration`, `is_active`) VALUES
	(1,'Quiz on Arrays',30,1);

INSERT INTO `questions`(`question`,`option_a`,`option_b`,`option_c`,`option_d`,`correct_option`) VALUES
	('What is A?','A','B','C','D',2),
	('What is B?','A','B','C','D',4),
	('What is C?','A','B','C','D',1),
	('What is D?','A','B','C','D',3),
	('What is E?','A','B','C','D',2),
	('What is F?','A','B','C','D',4);

INSERT INTO `quiz_questions`(`course_quiz_id`,`question_id`) VALUES
	(1,1),
	(1,2),
	(1,3),
	(1,4),
	(1,5),
	(1,6);

/* 
CREATE TABLE IF NOT EXISTS 
`dummy` (
	`id` int(11) AUTO_INCREMENT,
	PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1; 
*/