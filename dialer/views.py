import os
import subprocess
from subprocess import Popen, PIPE
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)
logger.info('Info log in views.py')

def file_list(request):
    # Define the directory where the files are stored
    directory = '/spark/filebrowser/reports/truecaller/'

    # Get a list of files in the directory
    files = sorted(os.listdir(directory), reverse=True)[:30]

    # Check if the form has been submitted
    if request.method == 'POST':
        # Get the selected file and text input from the form
        file_name = request.POST.get('file')
        text_input = request.POST.get('text_input')

        # Define the command to run the script on the selected file and text input
        #script_path = os.path.join(settings.BASE_DIR, 'dialer', 'scripts', 'truecaller.py')
        script_path = os.path.join(settings.BASE_DIR, 'dialer', 'scripts', 'dialer.py')
        command = ["python", script_path, file_name, text_input]

        # Run the script using subprocess
        print(command)
        #subprocess.run(command)
        process = subprocess.Popen([script_path, file_name, text_input, "10"])
        output = f"dialer started with pid {process.pid}"
        logger.info(output)

        # Redirect back to the file list page
        return redirect('file_list')

    # Pass the file list to the template context
    context = {'files': files}

    # Return the file list template with the form
    return render(request, 'file_list.html', context)

def file_process(request):
    # This view is not used for rendering a template
    # It is only used to handle the form submission from file_list

    # We should never get to this view without a POST request
    # But just to be safe, check the method
    if request.method == 'POST':
        # Get the selected file and text input from the form
        file_name = request.POST.get('file')
        text_input = request.POST.get('text_input')

        # Define the command to run the script on the selected file and text input
        #script_path = os.path.join(settings.BASE_DIR, 'dialer', 'scripts', 'truecaller.py')
        script_path = os.path.join(settings.BASE_DIR, 'dialer', 'scripts', 'dialer.py')
        command = [script_path, file_name, text_input]

        # Run the script using subprocess
        #print(command)
        #subprocess.run(command)
        process = subprocess.Popen([script_path, file_name, text_input, "10"])
        output = f"dialer started with pid {process.pid}"
        print(output)
        logger.info(output)
        context = {'output': output}
        #return redirect('file_process', output=output)
        return render(request, 'file_process.html', context)
        #return HttpResponse("File processed successfully: PID " + str(process.pid))
        # Redirect back to the file list page
        #return redirect('file_list')


