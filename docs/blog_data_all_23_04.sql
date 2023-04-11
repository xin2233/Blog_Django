/*
SQLyog Community v13.1.6 (64 bit)
MySQL - 8.0.28 : Database - blogdb
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`blogdb` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `blogdb`;

/*Table structure for table `auth_group` */

DROP TABLE IF EXISTS `auth_group`;

CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `auth_group` */

/*Table structure for table `auth_group_permissions` */

DROP TABLE IF EXISTS `auth_group_permissions`;

CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `auth_group_permissions` */

/*Table structure for table `auth_permission` */

DROP TABLE IF EXISTS `auth_permission`;

CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `auth_permission` */

insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values 
(1,'Can add log entry',1,'add_logentry'),
(2,'Can change log entry',1,'change_logentry'),
(3,'Can delete log entry',1,'delete_logentry'),
(4,'Can view log entry',1,'view_logentry'),
(5,'Can add permission',2,'add_permission'),
(6,'Can change permission',2,'change_permission'),
(7,'Can delete permission',2,'delete_permission'),
(8,'Can view permission',2,'view_permission'),
(9,'Can add group',3,'add_group'),
(10,'Can change group',3,'change_group'),
(11,'Can delete group',3,'delete_group'),
(12,'Can view group',3,'view_group'),
(13,'Can add user',4,'add_user'),
(14,'Can change user',4,'change_user'),
(15,'Can delete user',4,'delete_user'),
(16,'Can view user',4,'view_user'),
(17,'Can add content type',5,'add_contenttype'),
(18,'Can change content type',5,'change_contenttype'),
(19,'Can delete content type',5,'delete_contenttype'),
(20,'Can view content type',5,'view_contenttype'),
(21,'Can add session',6,'add_session'),
(22,'Can change session',6,'change_session'),
(23,'Can delete session',6,'delete_session'),
(24,'Can view session',6,'view_session'),
(25,'Can add 邮箱验证码',7,'add_emailverifyrecord'),
(26,'Can change 邮箱验证码',7,'change_emailverifyrecord'),
(27,'Can delete 邮箱验证码',7,'delete_emailverifyrecord'),
(28,'Can view 邮箱验证码',7,'view_emailverifyrecord'),
(29,'Can add 用户数据',8,'add_userprofile'),
(30,'Can change 用户数据',8,'change_userprofile'),
(31,'Can delete 用户数据',8,'delete_userprofile'),
(32,'Can view 用户数据',8,'view_userprofile'),
(33,'Can add 博客分类',9,'add_category'),
(34,'Can change 博客分类',9,'change_category'),
(35,'Can delete 博客分类',9,'delete_category'),
(36,'Can view 博客分类',9,'view_category'),
(37,'Can add 侧边栏',10,'add_sidebar'),
(38,'Can change 侧边栏',10,'change_sidebar'),
(39,'Can delete 侧边栏',10,'delete_sidebar'),
(40,'Can view 侧边栏',10,'view_sidebar'),
(41,'Can add 文章标签',11,'add_tag'),
(42,'Can change 文章标签',11,'change_tag'),
(43,'Can delete 文章标签',11,'delete_tag'),
(44,'Can view 文章标签',11,'view_tag'),
(45,'Can add 文章',12,'add_post'),
(46,'Can change 文章',12,'change_post'),
(47,'Can delete 文章',12,'delete_post'),
(48,'Can view 文章',12,'view_post');

/*Table structure for table `auth_user` */

DROP TABLE IF EXISTS `auth_user`;

CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `auth_user` */

insert  into `auth_user`(`id`,`password`,`last_login`,`is_superuser`,`username`,`first_name`,`last_name`,`email`,`is_staff`,`is_active`,`date_joined`) values 
(1,'pbkdf2_sha256$260000$KAFHDHhcm2vPAOIA313gX7$x0kmX4f5NDktMjqox8a6g7FyI1wC48cibfli8DRB7OM=','2023-03-10 06:55:55.866521',0,'zjxcyr@qq.com','','','zjxcyr@qq.com',0,1,'2023-03-10 06:55:07.191249'),
(2,'pbkdf2_sha256$260000$KSsGt0entaX0hDWe4pQnRt$OCTQdCtjyz6haKV92x+03euNDL6Wz2aWFl9cxvgB9Og=','2023-04-03 09:25:42.246290',1,'admin','','','123@qq.com',1,1,'2023-03-11 06:47:28.819973');

/*Table structure for table `auth_user_groups` */

DROP TABLE IF EXISTS `auth_user_groups`;

CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `auth_user_groups` */

/*Table structure for table `auth_user_user_permissions` */

DROP TABLE IF EXISTS `auth_user_user_permissions`;

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `auth_user_user_permissions` */

/*Table structure for table `blog_category` */

DROP TABLE IF EXISTS `blog_category`;

CREATE TABLE `blog_category` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `desc` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `add_date` datetime(6) NOT NULL,
  `pub_date` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `blog_category` */

insert  into `blog_category`(`id`,`name`,`desc`,`add_date`,`pub_date`) values 
(1,'vim','vim','2023-03-11 06:48:55.940754','2023-03-11 06:48:55.940754');

/*Table structure for table `blog_post` */

DROP TABLE IF EXISTS `blog_post`;

CREATE TABLE `blog_post` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(61) COLLATE utf8mb4_unicode_ci NOT NULL,
  `desc` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_hot` tinyint(1) NOT NULL,
  `pv` int NOT NULL,
  `add_date` datetime(6) NOT NULL,
  `pub_date` datetime(6) NOT NULL,
  `category_id` bigint NOT NULL,
  `owner_id` int NOT NULL,
  `tags_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `blog_post_category_id_c326dbf8_fk_blog_category_id` (`category_id`),
  KEY `blog_post_owner_id_ff7c9277_fk_auth_user_id` (`owner_id`),
  KEY `blog_post_tags_id_33214a08_fk_blog_tag_id` (`tags_id`),
  CONSTRAINT `blog_post_category_id_c326dbf8_fk_blog_category_id` FOREIGN KEY (`category_id`) REFERENCES `blog_category` (`id`),
  CONSTRAINT `blog_post_owner_id_ff7c9277_fk_auth_user_id` FOREIGN KEY (`owner_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `blog_post_tags_id_33214a08_fk_blog_tag_id` FOREIGN KEY (`tags_id`) REFERENCES `blog_tag` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `blog_post` */

insert  into `blog_post`(`id`,`title`,`desc`,`content`,`is_hot`,`pv`,`add_date`,`pub_date`,`category_id`,`owner_id`,`tags_id`) values 
(1,'gvim配置','gvim配置','<p>参考：</p><p><a href=\"https://www.cnblogs.com/ryzz/p/12554617.html\">gVim设置默认主题和字体（图文详细版） - RYZZ - 博客园 (cnblogs.com)</a></p><p>&nbsp;</p><blockquote><p>软件下载：https://pc.qq.com/detail/1/detail_3021.html&nbsp;</p></blockquote><h2>建议直接复制下面文章中的配置文件：</h2><p>gvim的字符集，编码等utf-8设置</p><p>&nbsp;1 \" 设置行号\r\n 2 set number\r\n 3 \r\n 4 \" 编码设置\r\n 5 set enc=utf-8\r\n 6 \" set fencs=utf-8\r\n 7 \" ,ucs-bom,shift-jis,gb18030,gbk,gb2312,cp936\r\n 8 &nbsp;\r\n 9 \" 设置菜单语言\r\n10 set langmenu=zh_CN.UTF-8\r\n11 &nbsp;\r\n12 \" 导入删除菜单脚本，删除乱码的菜单\r\n13 source $VIMRUNTIME/delmenu.vim\r\n14 &nbsp;\r\n15 \" 导入正常的菜单脚本\r\n16 source $VIMRUNTIME/menu.vim\r\n17 &nbsp;\r\n18 \" 设置提示信息语言\r\n19 language messages zh_CN.utf-8\r\n20 &nbsp;\r\n21 \" 字体设置\r\n22 set guifont=Consolas:h10:cANSI:qDRAFT\r\n23 \r\n24 \" 命令行（在状态行下）的高度，默认为1，这里是2\r\n25 \" set cmdheight=2\r\n26 \r\n27 \" 设置搜索大小写不敏感\r\n28 set ignorecase\r\n29 \r\n30 \" hi CursorLine term=bold cterm=bold ctermbg=Red\r\n31 \" 当前行不仅被高亮成了红色，而且还变成了粗体，这就是命令中bold和Red的效果，其中cterm=bold就是指定在终端中被高亮的行变为粗体，而 ctermbg=Red就是指定高亮行在终端中的背景色，其他的选项还有ctermfg(前景色)，guibg(gvim中的背景色)等等，这里就不赘述了。\r\n32 \" 设置当前行高亮\r\n33 set cursorline \r\n34 \" cterm：【bold粗体】，guibg【gvim中的背景色】，ctermbg=Red【指定高亮行在终端中的背景色】，ctermfg【前景色】，\r\n35 hi CursorLine &nbsp; cterm=NONE ctermbg=darkred ctermfg=white \r\n36 hi CursorColumn cterm=NONE ctermbg=darkred ctermfg=white&nbsp;</p><p>&nbsp;</p><p>有更多想更改的，参考下面连接：</p><p><a href=\"https://blog.csdn.net/u010074478/article/details/35987479\">(14条消息) gvim的字符集，编码等utf-8设置_爱菜鸟高高飞的博客-CSDN博客_gvim utf8</a></p><p>&nbsp;</p><h2>问题1：解决方法。</h2><p><a href=\"https://blog.csdn.net/guyue35/article/details/103426391\">(14条消息) gvim菜单栏乱码解决办法_guyue35的博客-CSDN博客_gvim 乱码</a></p><p>&nbsp;</p><p>enc：</p><p>1. encoding<br>&nbsp;&nbsp;&nbsp; 表示vim自身内部使用的编码方式，如内部缓冲，菜单，消息等的编码方式。如果你现在正以不同于encoding的编码编辑一个文件，如使用set，它并不决定文件被保存的编码方式，也不能指导vim我们要打开的文件是什么格式。它不是作这个用的。</p><p>&nbsp;</p><p>2. fileencoding<br>&nbsp;&nbsp;&nbsp; 表示VIM所认为的当前被处理的文件的编码格式，即告诉我们当前打开的文件的格式。而且如果我们保存文件的话，vim也会以此格式保存，就算这个fileencoding并不是真正的fileencoding。举个例子，有个文件是utf-8编码，而且我们的vim将他成功打开了，即vim识别出他是utf-8编码，这样我们在vim里面执行:set fileencoding命令得到的结果就是fileencoding=utf-8，可见vim已经识别出了这个文件的格式，而且以此格式对文件操作，如果我们手动修改fileencoding即：执行:set fileencoding=cp936的话，然后保存文件，得到的文件就将自动被转换成了cp936格式，可以用file filename命令来查看该文件的格式，的确如此。如果还想转换回来，就可以像刚才那样再次用vim打开，然后:set fileencoding=utf-8然后保存，当然也可以用iconv命令即：<br>iconv -f cp936 -t utf-8 -o targetfile sourcefile 即将按照cp936格式编码的文件sourcefile转换成按照utf-8编码的文件targetfile. 此外，不管你怎么变换，我们一直没有改动encoding，而且使用:set encoding命令查看其值，也是一直没有变，它的值如果我们不人工指定的话，一般来说默认等于我们的LANG里面的设置的字符集，我们目前默认的LANG=en_US.UTF-8，encoding一般会与LANG的locale设置保持一致的。可见，不管你认为文件是什么格式，我的encoding一直不变，那么我再进行文件处理的时候，就会在内部用一种格式，即encoding指定的格式，当然首先要从fileencoding指定的格式转换成encoding的格式，处理后，在转换成fileencoding的格式，具体的转换依赖的是iconv的功能。<br>&nbsp; &nbsp; 那么，fileencoding的格式我们总不能每打开一个文件手动指定吧，vim时可以自动检查的，当检查成功后，就会自动设置fileencoding的值，这就是fileencodings的功能。&nbsp;</p><p>&nbsp;</p><p>3. fileencodings<br>&nbsp;&nbsp;&nbsp; 这是一个列表，他一般包含多个值，VIM在打开文件的时候会从这个列表中依次拿出一个值与被打开的文件比较，直到找到匹配的编码方式a。然后fileencoding就会被设置成a。这样当你对文件编辑的时候就会使用a.<br><br>下面是一段网上的介绍的摘抄：<br>vim里面的编码主要跟三个参数有关：enc(encoding), fenc(fileencoding)和fencs(fileencodings)<br>其中fenc是当前文档的编码，也就是说，一个在vim里面已正确显示了的文档(前提是您的系统环境跟您的enc配置匹配)，您能够通过改变fenc后再w来将此文档存成不同的编码。比如说，我:set fenc=utf-8然后:w就把文档存成utf-8的了，:setfenc=gb18030再:w就把文档存成gb18030的了。这个值对于打开文档的时候是否能够正确地解码没有任何关系。<br>fencs就是用来在打开文档的时候进行解码的猜测列表。文档编码没有百分百正确的判断方法，所以vim只能猜测文档编码。比如我的vimrc里面这个的配置是<br>set fileencodings=utf-8,gb18030,utf-16,big5<br>所以我的vim每打开一个文档，先尝试用utf-8进行解码，假如用utf-8解码到了一半出错(所谓出错的意思是某个地方无法用utf-8正确地解码)，那么就从头来用gb18030重新尝试解码，假如gb18030又出错(注意gb18030并不是像utf-8似的规则编码，所以所谓的出错只是说某个编码没有对应的有意义的字，比如0)，就尝试用utf-16，仍然出错就尝试用big5。这一趟下来，假如中间的某次解码从头到尾都没有出错，那么vim就认为这个文档是这个编码的，不会再进行后面的尝试了。这个时候，fenc的值就会被设为vim最后采用的编码值，能够用:setfenc?来查看具体是什么。<br>当然这个也是有可能出错的，比如您的文档是gb18030编码的，但是实际上只有一两个字符是中文，那么有可能他们正好也能被utf-8解码，那么这个文档就会被误认为是utf-8的导致错误解码。<br>至于enc，其作用基本只是显示。不管最后的文档是什么编码的，vim都会将其转换为当前系统编码来进行处理，这样才能在当前系统里面正确地显示出来，因此enc就是干这个的。在windows下面，enc默认是cp936，这也就是中文windows的默认编码，所以enc是无需改的。在linux下，随着您的系统locale可能设为zh_CN.gb18030或zh_CN.utf-8，您的enc要对应的设为gb18030或utf-8(或gbk之类的)。<br>最后再来说一下新建空文档的默认编码。看文档似乎说会采用fencs里面的第一个编码作为新建文档的默认编码。但是这里有一个问题，就是fencs的顺序跟解码成功率有很大关系，根据我的经验utf-8在前比gb18030在前成功率要高一些，那么假如我新建文档默认想让他是gb18030编码怎么办？一个方法是每次新建文档后都:set fenc=gb18030一下，但是我发现在vimrc里面配置fenc=gb18030也能达到这个效果。<br>总结一下，我的vimrc里面的配置是：<br>set fileencoding=gb18030<br>set fileencodings=utf-8,gb18030,utf-16,big5</p><p>另外enc根据环境来设。</p>',0,9,'2023-03-11 06:49:56.392544','2023-03-11 06:57:19.247673',1,2,1);

/*Table structure for table `blog_sidebar` */

DROP TABLE IF EXISTS `blog_sidebar`;

CREATE TABLE `blog_sidebar` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `display_type` int unsigned NOT NULL,
  `content` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `sort` int unsigned NOT NULL,
  `status` int unsigned NOT NULL,
  `add_date` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `blog_sidebar_chk_1` CHECK ((`display_type` >= 0)),
  CONSTRAINT `blog_sidebar_chk_2` CHECK ((`sort` >= 0)),
  CONSTRAINT `blog_sidebar_chk_3` CHECK ((`status` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `blog_sidebar` */

/*Table structure for table `blog_tag` */

DROP TABLE IF EXISTS `blog_tag`;

CREATE TABLE `blog_tag` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `add_date` datetime(6) NOT NULL,
  `pub_date` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `blog_tag` */

insert  into `blog_tag`(`id`,`name`,`add_date`,`pub_date`) values 
(1,'vim','2023-03-11 06:49:07.496144','2023-03-11 06:49:07.496144');

/*Table structure for table `django_admin_log` */

DROP TABLE IF EXISTS `django_admin_log`;

CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `django_admin_log` */

insert  into `django_admin_log`(`id`,`action_time`,`object_id`,`object_repr`,`action_flag`,`change_message`,`content_type_id`,`user_id`) values 
(1,'2023-03-11 06:48:55.962191','1','vim',1,'[{\"added\": {}}]',9,2),
(2,'2023-03-11 06:49:07.517132','1','vim',1,'[{\"added\": {}}]',11,2),
(3,'2023-03-11 06:49:56.433299','1','gvim配置',1,'[{\"added\": {}}]',12,2),
(4,'2023-03-11 06:52:19.355771','1','gvim配置',2,'[]',12,2),
(5,'2023-03-11 06:57:19.282110','1','gvim配置',2,'[{\"changed\": {\"fields\": [\"\\u6587\\u7ae0\\u8be6\\u60c5\"]}}]',12,2),
(6,'2023-03-11 06:57:56.619700','2','gvim',3,'',12,2);

/*Table structure for table `django_content_type` */

DROP TABLE IF EXISTS `django_content_type`;

CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `django_content_type` */

insert  into `django_content_type`(`id`,`app_label`,`model`) values 
(1,'admin','logentry'),
(3,'auth','group'),
(2,'auth','permission'),
(4,'auth','user'),
(9,'blog','category'),
(12,'blog','post'),
(10,'blog','sidebar'),
(11,'blog','tag'),
(5,'contenttypes','contenttype'),
(6,'sessions','session'),
(7,'users','emailverifyrecord'),
(8,'users','userprofile');

/*Table structure for table `django_migrations` */

DROP TABLE IF EXISTS `django_migrations`;

CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `django_migrations` */

insert  into `django_migrations`(`id`,`app`,`name`,`applied`) values 
(1,'contenttypes','0001_initial','2023-03-10 06:51:08.768411'),
(2,'auth','0001_initial','2023-03-10 06:51:11.225064'),
(3,'admin','0001_initial','2023-03-10 06:51:11.921134'),
(4,'admin','0002_logentry_remove_auto_add','2023-03-10 06:51:11.977954'),
(5,'admin','0003_logentry_add_action_flag_choices','2023-03-10 06:51:12.039627'),
(6,'contenttypes','0002_remove_content_type_name','2023-03-10 06:51:12.417667'),
(7,'auth','0002_alter_permission_name_max_length','2023-03-10 06:51:12.606319'),
(8,'auth','0003_alter_user_email_max_length','2023-03-10 06:51:12.704390'),
(9,'auth','0004_alter_user_username_opts','2023-03-10 06:51:12.773136'),
(10,'auth','0005_alter_user_last_login_null','2023-03-10 06:51:12.924121'),
(11,'auth','0006_require_contenttypes_0002','2023-03-10 06:51:12.975009'),
(12,'auth','0007_alter_validators_add_error_messages','2023-03-10 06:51:13.030821'),
(13,'auth','0008_alter_user_username_max_length','2023-03-10 06:51:13.233740'),
(14,'auth','0009_alter_user_last_name_max_length','2023-03-10 06:51:13.474873'),
(15,'auth','0010_alter_group_name_max_length','2023-03-10 06:51:13.570957'),
(16,'auth','0011_update_proxy_permissions','2023-03-10 06:51:13.707171'),
(17,'auth','0012_alter_user_first_name_max_length','2023-03-10 06:51:13.925363'),
(18,'blog','0001_initial','2023-03-10 06:51:15.292358'),
(19,'sessions','0001_initial','2023-03-10 06:51:15.545400'),
(20,'users','0001_initial','2023-03-10 06:51:16.257425');

/*Table structure for table `django_session` */

DROP TABLE IF EXISTS `django_session`;

CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `django_session` */

insert  into `django_session`(`session_key`,`session_data`,`expire_date`) values 
('qnzznzs5a3vx2drfvsipgu7y437penyi','.eJxVjDsOwjAQBe_iGlnOGn9CSZ8zWLvrDQ4gR4qTCnF3iJQC2jcz76USbmtJW5MlTVldFKjT70bID6k7yHest1nzXNdlIr0r-qBND3OW5_Vw_w4KtvKto3AeGSmI8dGeO8HgyEMQsB1zJGchRjEAtrfGB8d9YLLOEIwYszfq_QHucDef:1pat1p:gPPpYwW7XPbH0NUh5598bkc_DIeC7ZaujcU8CmGBSkw','2023-03-25 06:48:29.752589'),
('z8p6qjqwhtgw5xjiuj3ndocqday8qe4i','.eJxVjDsOwjAQBe_iGlnOGn9CSZ8zWLvrDQ4gR4qTCnF3iJQC2jcz76USbmtJW5MlTVldFKjT70bID6k7yHest1nzXNdlIr0r-qBND3OW5_Vw_w4KtvKto3AeGSmI8dGeO8HgyEMQsB1zJGchRjEAtrfGB8d9YLLOEIwYszfq_QHucDef:1pi8tS:6RnCxBs6D7v45I7xD8A1Tla4dz5qGdS3KTOTKsX4EKQ','2023-04-14 07:09:50.767340'),
('ztsc6l31udefev91udqwvelzsdxf92jv','.eJxVjDsOwjAQBe_iGlnOGn9CSZ8zWLvrDQ4gR4qTCnF3iJQC2jcz76USbmtJW5MlTVldFKjT70bID6k7yHest1nzXNdlIr0r-qBND3OW5_Vw_w4KtvKto3AeGSmI8dGeO8HgyEMQsB1zJGchRjEAtrfGB8d9YLLOEIwYszfq_QHucDef:1pjGRa:P1DHk3K5XwmI8gz-Gn-Z5YR1gmXxgMh4IeKRSCY1snw','2023-04-17 09:25:42.276547');

/*Table structure for table `users_emailverifyrecord` */

DROP TABLE IF EXISTS `users_emailverifyrecord`;

CREATE TABLE `users_emailverifyrecord` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `code` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `send_type` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `send_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `users_emailverifyrecord` */

insert  into `users_emailverifyrecord`(`id`,`code`,`email`,`send_type`,`send_time`) values 
(1,'DE7aSjQg','zjxcyr@qq.com','register','2023-03-10 06:55:07.701930');

/*Table structure for table `users_userprofile` */

DROP TABLE IF EXISTS `users_userprofile`;

CREATE TABLE `users_userprofile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nike_name` varchar(23) COLLATE utf8mb4_unicode_ci NOT NULL,
  `birthday` date DEFAULT NULL,
  `gender` varchar(6) COLLATE utf8mb4_unicode_ci NOT NULL,
  `address` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `image` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `desc` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `gexing` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `owner_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `owner_id` (`owner_id`),
  CONSTRAINT `users_userprofile_owner_id_75836c59_fk_auth_user_id` FOREIGN KEY (`owner_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `users_userprofile` */

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
