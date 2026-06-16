import os


# routine to return an application string dependent on the file type.
def find_application(filename):
    fn, ext = os.path.splitext(filename)
    if ext == '.pdf':
        application = 'application/pdf'
    elif ext == '.docx':
        application = 'application/application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    elif ext == '.pptx':
        application = 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
    elif ext == '.xlsx':
        application = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    elif ext == '.jpeg':
        application = 'image/jpeg'
    else:
        application = 'text/plain'

    return application
