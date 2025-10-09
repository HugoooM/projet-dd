sudo apt update
sudo apt upgrade
sudo apt install -y postgresql postgresql-contrib
sudo -u postgres psql -f postgresql/schema/script_init.sql
sudo psql -U blog_user -d blog_db -h localhost
# mot de passe postgre : postgresql