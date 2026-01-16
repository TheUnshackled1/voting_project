from votes.models import Vote
import re

qs = Vote.objects.filter(voter_name='Anonymous').exclude(voter_email__isnull=True).exclude(voter_email='')
count = 0
for v in qs:
    local = v.voter_email.split('@', 1)[0]
    name = ' '.join([p.capitalize() for p in re.split(r'[._\-]+', local) if p])
    v.voter_name = name or 'Anonymous'
    v.save()
    count += 1
print(f'Updated {count} vote(s)')
