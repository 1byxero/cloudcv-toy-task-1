from django.http import HttpResponse
from django.shortcuts import render,redirect
from forms import DocumentForm
from models import Document
from os import path,system
from django.conf import settings
from opencvstuff import *
import subprocess
#foregroundextraction,imagegradient,smoothing





# Create your views here.

def index(request):
	if request.method=="POST":		
		form = DocumentForm(request.POST, request.FILES)
		if form.is_valid():
			newdoc = Document(docfile = request.FILES['docfile'])
			newdoc.save()
			question = form.cleaned_data['question']
			renderthis = process(newdoc.docfile.name,question)
			imageurlcontainer = renderthis[0]						
			anstemp = renderthis[1]
			anstemp = anstemp.split("\n")
			print anstemp
			ans = anstemp[-2].strip()
			return render(request,'polls/showimg.html',{"imageurlcontainer":imageurlcontainer,"ans":ans,"question":question})	
		else:			
			return HttpResponse("Error brah")		
	else:
		system("pwd")
		form = DocumentForm()
		documents = Document.objects.all()			
		return render(request,'polls/index.html',{"form":form})



def process(name=None,question=""):	
	if name==None or len(question)==0:
		return redirect(index)
	else:
		filepath = path.join(settings.MEDIA_ROOT,name)		
		if path.isfile(filepath):			
			#change the directory here to apt directory using chdir
			proc = subprocess.Popen([ "th predict.lua -checkpoint_file checkpoints/emb512_epoch23.26_0.4610_cpu.t7 -input_image_path media/"+str(name)+" -question '"+str(question)+"?'"], stdout=subprocess.PIPE, shell=True)
			(out, err) = proc.communicate()					
			output = [[name],out]						
			return output
		else:
			return HttpResponse("Some Error Error Occured")

