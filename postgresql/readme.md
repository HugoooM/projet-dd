sudo apt update
sudo apt install -y postgresql postgresql-contrib
sudo -u postgres psql -f postgresql/schema/script_init.sql
psql -U blog_user -d blog_db -h localhost
mot de passe postgre : postgresql