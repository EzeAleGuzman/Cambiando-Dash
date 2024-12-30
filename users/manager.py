from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, name,lastname, email, password, **extra_fields):
        """
        Create and save a User with the given username, email and password.
        """
        if not name or not lastname or not email:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(name=name, lastname=lastname, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, name, lastname, email, password, **extra_fields):
        """ 
        Create and save a regular user with the given name, lastname, email, password.
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', False)
        return self._create_user(name, lastname, email, password, **extra_fields)
     
    
    def create_superuser(self, name, lastname, email, password, **extra_fields):
        """ 
        Create a super user (root), with minimum required args:
        name, last name, email, password
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True.')
        
        return self._create_user(name, lastname, email, password, **extra_fields)
    
        