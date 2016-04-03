mysql --user=root --password='' -e "GRANT USAGE ON *.* TO 'ags_user'@'localhost';"
mysql --user=root --password='' -e "DROP USER 'ags_user'@'localhost';"
mysql --user=root --password='' -e "CREATE USER 'ags_user'@'localhost';"
mysql --user=root --password='' -e "GRANT ALL PRIVILEGES ON *.* TO 'ags_user'@'localhost' WITH GRANT OPTION;"
mysql --user=root --password='' -e "UPDATE mysql.user SET Password=PASSWORD('123456') WHERE User='ags_user';"
mysql --user=root --password='' -e "FLUSH PRIVILEGES;"
mysql --user=root --password='' -e "grant all on *.* to ags_user@'%' identified by '123456';"
mysql --user=root --password='' -e "DROP DATABASE IF EXISTS auto_google_search; CREATE DATABASE auto_google_search DEFAULT CHARACTER SET utf8; USE auto_google_search;"
echo 'db.auto_google_search.user' > /root/db.auto_google_search.user
