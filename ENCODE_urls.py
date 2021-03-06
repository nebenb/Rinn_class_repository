import pandas as pd

column=['experiment_target', 'file_accession', 'experiment_accession', 'paired_end', 'paired_with', 'md5sum', 'URL', 'control']
df=pd.read_csv('filtered_tf_metadata.csv', names=column)
#df=df.drop(columns=['experiment_target', 'paired_end', 'md5sum'])
a=pd.DataFrame()
# Find files that are paired and zip together
for x in df['file_accession']:
	for y in df['paired_with']:
		if x == y:
			#b=(df.loc[df['file_accession'] == y], df.loc[df['paired_with'] == x])
			a=a.append([df.loc[df['file_accession'] == y], df.loc[df['paired_with'] == x]])

#Drop duplicate rows
a=a.drop_duplicates()
a=a.drop(columns=['paired_end', 'paired_with', 'file_accession', 'experiment_accession', 'md5sum'])	
#Build Control URLs
beg_url='https://www.encodeproject.org'
control=[]

for item in a['control']:
    item=beg_url+str(item)
    control.append(item)

middle_url='@@download/'
control_2=[]

for item in control:
    item=str(item)+middle_url
    control_2.append(item)

control_3=[]

for item in control:
    item=item[-12:-1]
    control_3.append(item)

control_4=[]
    
for x, y in zip(control_2, control_3):
    x=x+y
    control_4.append(x)

control_5=[]

for item in control_4:
    item=item+'.fastq.gz'
    control_5.append(item)

a['control']=control_5

#Set index to replicates
a_lst=list(a['experiment_target'])
res = [] 
for i in a_lst: 
    if i not in res: 
        res.append(i)

uniq=[]
for item in res:
	num=a_lst.count(item)
	uniq.append(num)

lst=[]
fastq=[]
for number in uniq:
    for _ in range(int(number/2)):
        st1="rep"+str(_)
        st2="rep"+str(_)
        lst.append(st1)
        lst.append(st2)
        fastq.append('fastq 1')
        fastq.append('fastq 2')

control=[]
for item in a['control']:
    if len(item) < 70:
        item = 'n/a'
        control.append(item)
    else:
        control.append(item)
a['control']=control
   
	
a['replicate']=lst
a['fastq']=fastq
#a=a.set_index('experiment_target')
a=a.reindex(columns=['experiment_target','replicate', 'fastq', 'URL', 'control'])

a.to_csv('python_tf_output.csv')


#Merge rows according to provided datasheet format
df=pd.DataFrame(columns=['target', 'replicate', 'fastq1', 'fastq2', 'control1', 'control2'])

a_fastq1=a.loc[a['fastq'] == 'fastq 1']
a_fastq2=a.loc[a['fastq'] == 'fastq 2']

df['target']=a_fastq1['experiment_target']
df=df.set_index('target')
a_fastq1=a_fastq1.set_index('experiment_target')
a_fastq2=a_fastq2.set_index('experiment_target')

df['replicate']=a_fastq1['replicate']
df['fastq1']=a_fastq1['URL']
df['fastq2']=a_fastq2['URL']
df['control1']=a_fastq1['control']
df['control2']=a_fastq2['control']

df.to_csv('design.csv')


	

