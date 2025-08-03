from django.core.management.base import BaseCommand
from authentication.models import User


class Command(BaseCommand):
    help = 'Create sample users for testing'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=5,
            help='Number of sample users to create',
        )
    
    def handle(self, *args, **options):
        count = options['count']
        
        # Sample user data
        sample_users = [
            {
                'username': 'john_doe',
                'email': 'john.doe@example.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'role': 'user',
                'password': 'userpass123'
            },
            {
                'username': 'jane_smith',
                'email': 'jane.smith@example.com',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'role': 'user',
                'password': 'userpass123'
            },
            {
                'username': 'admin_user',
                'email': 'admin.user@example.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'role': 'admin',
                'password': 'adminpass123'
            },
            {
                'username': 'test_manager',
                'email': 'manager@example.com',
                'first_name': 'Test',
                'last_name': 'Manager',
                'role': 'admin',
                'password': 'managerpass123'
            },
            {
                'username': 'demo_user',
                'email': 'demo@example.com',
                'first_name': 'Demo',
                'last_name': 'User',
                'role': 'user',
                'password': 'demopass123'
            },
        ]
        
        created_count = 0
        
        for i in range(min(count, len(sample_users))):
            user_data = sample_users[i]
            
            # Check if user already exists
            if User.objects.filter(email=user_data['email']).exists():
                self.stdout.write(
                    self.style.WARNING(f'User {user_data["email"]} already exists')
                )
                continue
            
            if User.objects.filter(username=user_data['username']).exists():
                self.stdout.write(
                    self.style.WARNING(f'Username {user_data["username"]} already exists')
                )
                continue
            
            # Create user
            password = user_data.pop('password')
            user = User.objects.create_user(**user_data)
            user.set_password(password)
            user.save()
            
            created_count += 1
            self.stdout.write(
                self.style.SUCCESS(
                    f'Created {user_data["role"]} user: {user.email}'
                )
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} sample users')
        )
