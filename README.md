#oldfashion

docker powered mini paas


##Installation

 - run `bootstrap.sh`
 - sudo pip install oldfashion

##Uploading SSH key

	cat ~/.ssh/id_rsa.pub | ssh <USER>@<OLDFASHION_HOST> "oldfashion acl add <KEY_NAME>"
 
##Supported app types

 - [django](https://www.djangoproject.com)
 - [nodejs](https://nodejs.org)
 
##Usage

    git clone git@github.com:heroku/node-js-sample.git
    git remote add oldfashion@<OLDFASHION_HOST>:<APP_NAME>
    git push oldfashion master
    
In response you should see something like this

    git push oldfashion master
    Counting objects: 388, done.
    Delta compression using up to 4 threads.
    Compressing objects: 100% (313/313), done.
    Writing objects: 100% (388/388), 213.57 KiB | 0 bytes/s, done.
    Total 388 (delta 46), reused 388 (delta 46)
    remote: ----> Exporting code
    remote:       Cloning into /tmp/tmpYoy1jZ
    remote: ----> Building node-js-sample app

	..................
	
	remote: ----> Running
	remote: ----> Handling nginx
	remote:       Hostname oldfashion.im
	remote:       Reloading nginx configuration
	remote: ----> Cleanup
	remote:       Cleaning old containers
	remote:       Cleaning tmp files
	remote: ----> App is running at http://node-js-sample.oldfashion.im
	
