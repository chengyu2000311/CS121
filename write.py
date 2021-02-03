import shelve
import re, os
from urllib.parse import urlparse
from PartA import tokenize, computeWordFrequencies
from collections import defaultdict
stopWord= '''
a 
about
above
after
again
against
all
am
an
and
any
are
aren't
as
at
be
because
been
before
being
below
between
both
but
by
can't
cannot
could
couldn't
did
didn't
do
does
doesn't
doing
don't
down
during
each
few
for
from
further
had
hadn't
has
hasn't
have
haven't
having
he
he'd
he'll
he's
her
here
here's
hers
herself
him
himself
his
how
how's
i
i'd
i'll
i'm
i've
if
in
into
is
isn't
it
it's
its
itself
let's
me
more
most
mustn't
my
myself
no
nor
not
of
off
on
once
only
or
other
ought
our
ours
ourselves
out
over
own
same
shan't
she
she'd
she'll
she's
should
shouldn't
so
some
such
than
that
that's
the
their
theirs
them
themselves
then
there
there's
these
they
they'd
they'll
they're
they've
this
those
through
to
too
under
until
up
very
was
wasn't
we
we'd
we'll
we're
we've
were
weren't
what
what's
when
when's
where
where's
which
while
who
who's
whom
why
why's
with
won't
would
wouldn't
you
you'd
you'll
you're
you've
your
yours
yourself
yourselves'''

def writeReport():
    try:
        if os.path.exists("summary.txt"):
            os.remove('summary.txt')
        if os.path.exists("all_content.txt"):
            os.remove('all_content.txt')

        s = shelve.open('urlText.db')
        f = open('summary.txt', 'w')
        f1 = open('all_content.txt', 'w')

        f.write(f'There are {len(s)} pages found\n')
        f.write('------------------above are pages found------------------------------------------------\n')
        longest = 0
        longest_url = ''
        subdomain = defaultdict(int)
        for url, content in s.items():
            parsed = urlparse(url)
            if re.match('.+\.ics\.uci\.edu', parsed.netloc) and parsed.netloc != 'www.ics.uci.edu':
                subdomain[parsed.netloc.lower()] += 1

            for word in stopWord.split():
                if word in content:
                    break
            else:
                continue

            f1.write(content+'\n')
         
            if longest < len(content.split()):
                longest = len(content.split())
                longest_url = url

        for k, v in sorted(subdomain.items(), key=lambda x: x[0]):
            f.write(f'http://{k}, {v}\n')

        f.write(f'------------------above are {len(subdomain)} subdomains------------------------------------------------\n')
        f.write(f'The page that has most words is {longest_url}, and it has {longest} words\n')
        f.write('------------------above are longest page----------------------------------------------\n')
        f1.close()

        i = 1
        the_dict = computeWordFrequencies(tokenize('all_content.txt'))
        for key, value in sorted(the_dict.items(), key=lambda x:-x[1]):
            if key in stopWord: continue
            if i > 50: break
            i += 1
            f.write(f'{key}->{value}\n')
        f.write('------------------above are 50 top words except English stop word---------------------\n')
        
    except:
        f.write("Error occurs\n")

    finally:
        s.close()
        f.close()

