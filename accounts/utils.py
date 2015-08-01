def normalize_email(email):
	"""
	The point of this method is to lowercase the
	email address for storage in db. An argument 
	could be made that uppercased addresses are 
	different.
	"""
	clean_email = email.strip()
	if '@' in clean_email:
		first, second = clean_email.split('@')
		return '%s@%s' % (first.lower(), second.lower(),)
	return clean_email
