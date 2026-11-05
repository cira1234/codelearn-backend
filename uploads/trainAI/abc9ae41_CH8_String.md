## หน้า 1
บทที่8
ข้อมูลชนิดสตริง(String)
1
(หน้านี้มีรูปภาพ ข้อความด้านบนไม่รวมเนื้อหาในรูป)

## หน้า 2
ข้อมูลชนิดสตริง(String)
•
คือ อักขระที่เรียงต่อกันเป็นข้อความ และอยู่ภายใต้เครื่องหมาย “ ” 
(Double quote) เพื่อเก็บข้อความ เช่น ชื่อ นามสกุล ที่อยู่ เบอร์โทรศัพท์ ฯลฯ
•
โดยการน าอาร์เรย์ที่เก็บข้อมูลชนิดอักขระ (Array of Char) มาประยุกต์
เพื่อเก็บข้อความ และต้องมี \0 (Null character) ปิดท้ายข้อความเสมอ
2
Charles Babbage
0-2549-4990-2
Computer Programming
Rajamangala University of Technology Thanyaburi
39 Moo 1, Klong 6, Khlong Luang Pathum Thani 12110 Thailand

## หน้า 3
การประกาศตัวแปรชนิดสตริง
ตัวอย่าง
char Road[100];
char Name[50], Address[50]; 
char FirstName[15] = "Mr.ComEng" ;
char PhoneNo[ ] = "0281882169" ;
char PhoneNo[ ] = {'0', '2', '8', '1', '8', '8', 
'2', '1', '6', '9', '\0' } ;
3
char ชื่อตัวแปร[ขนาด] ;

## หน้า 4
ขนาดของสตริง (Size) = จ านวนตัวอักษร + 1
4
#include <stdio.h>
int main(){
char msg[] = "123";
printf(“Size of %s = %u\n", msg, (unsigned)sizeof(msg));
return 0;
}
1
2
3
4
5
6
ผลการท างาน
msg[0]
‘1’
msg[1]
‘2’
msg[2]
‘3’
msg[3]
‘\0’
Size of 123 = 4

## หน้า 5
ขนาดสตริง (Size) = จ านวนตัวอักษร + 1
5
#include <stdio.h>
int main(){
char msg[] = "AB\tC";
printf(“Size of %s = %u\n", msg, (unsigned)sizeof(msg));
return 0;
}
1
2
3
4
5
6
ผลการท างาน
msg[0]
‘A’
msg[1]
‘B’
msg[2]
‘\t’
msg[3]
‘C’
msg[4]
‘\0’
Size of AB      C = 5

## หน้า 6
ขนาดสตริง (Size) = จ านวนตัวอักษร + 1
6
#include <stdio.h>
int main(){
char msg[] = "abc\0def";
printf(“Size of %s = %u\n", msg, (unsigned)sizeof(msg));
return 0;
}
1
2
3
4
5
6
ผลการท างาน
[0]
[1]
[2]
[3]
[4]
[5]
[6]
[7]
msg
‘a’
‘b’
‘c’
‘\0’
‘d’
‘e’
‘f’
‘\0’
Size of abc = 8

## หน้า 7
การใช้ฟังก์ชันscanf( ) และgets( ) รับข้อมูลสตริง
7
#include <stdio.h> 
int main(void){ 
char str[25]; 
printf("Input: "); 
scanf("%s", str); 
printf("Output: %s\n", str); 
return 0; 
} 
1
2
3
4
5
6
7
8
#include <stdio.h> 
int main(void){ 
char str[25]; 
printf("Input: "); 
gets(str); 
printf("Output: %s\n", str); 
return 0; 
} 
1
2
3
4
5
6
7
8
ผลการท างาน
ผลการท างาน
Input: Computer Engineer
Output: Computer
Input: Computer Engineer
Output: Computer Engineer

## หน้า 8
ตัวอย่าง
8
#include <stdio.h>
int main(void){
char str[5];
str[0]= 'C';
str[1]= 'P';
str[2]= 'E';
str[3]= '\0';
printf("The message is [%s]",str);
return(0);
} 
1
2
3
4
5
6
7
8
9
10
ผลการท างาน
str[0]
‘C’
str[1]
‘P’
str[2]
‘E’
str[3]
‘\0’
str[4]
0
The message is [CPE]

## หน้า 9
ตัวอย่าง
9
#include <stdio.h>
int main(void){
char str[80];
int i;
printf("Enter a string : ");
gets(str);
for (i=0;str[i];i++)
printf("[%d] = %c (%d)\n", i, str[i], str[i]);
return(0);
} 
1
2
3
4
5
6
7
8
9
10
Enter a string : I'm free.
[0] = I (73)
[1] = ' (39)
[2] = m (109)
[3] =   (32)
[4] = f (102)
[5] = r (114)
[6] = e (101)
[7] = e (101)
[8] = . (46)
ผลการท างาน
[0]
[1]
[2]
[3]
[4]
[5]
[6]
[7]
[8]
[9]
msg
'I'
'\''
'm'
' '
'f'
'r'
'e'
'e'
'.'
'\0'
'\0' = null = 0 = False

## หน้า 10
ตัวอย่าง
10
#include <stdio.h>
char msg[21];
int i=0;
int main(void){   
printf("Enter your message : ");
gets(msg);
while(msg[i] != '\0'){
i++;
}
printf("Message Length = %d\n", i);
return(0);
}
1
2
3
4
5
6
7
8
9
10
11
12
Enter your message : Eric Clapton
Message Length =
ผลการท างาน
12
โปรแกรมท างานเหมือนฟังก์ชัน strlen

## หน้า 11
ฟังก์ชันจัดการข้อความ ใน <string.h>
11
ฟังก์ชัน
ค าอธิบาย
strlen(str)
หาความยาวของข้อความ
strcpy(str1, str2)
คัดลอกข้อความจากstr2 ไปเก็บที่str1
strcat(str1, str2)
ต่อข้อความstr1 ด้วยstr2
strcmp(str1, str2)
เปรียบเทียบตัวอักษรในข้อความ(Case 
sensitive) โดยเปรียบเทียบทีละตัวจากซ้ายไปขวา
ถ้า str1 = str2 จะคืนค่า = 0
ถ้า str1 < str2 จะคืนค่า < 0
ถ้า str1 > str2 จะคืนค่า > 0
(หน้านี้มีรูปภาพ ข้อความด้านบนไม่รวมเนื้อหาในรูป)

## หน้า 12
ตัวอย่างการใช้ฟังก์ชัน strcpy และ strcat
12
#include <stdio.h>
#include <string.h>
int main(){ 
char str1[60] = "sequence of characters ";
char str2[60] = "and can contain letters";
char str3[60];
strcpy(str3, str1);
strcat(str1, str2);
printf("str1 = %s\n", str1);
printf("str3 = %s\n", str3);
return(0);
}
1
2
3
4
5
6
7
8
9
10
11
12
13
14
ผลการท างาน
str1 = sequence of characters and can contain letters
str3 = sequence of characters 
ไม่สามารถใช้ str3 = str1 ได้

## หน้า 13
ตัวอย่างการใช้ฟังก์ชัน strcmp และ strlen
13
#include <stdio.h>
#include <string.h>
int main(){
char msg1[] = "Nanometer", msg2[] = "Nanometer";
int ptr;
printf("msg1 : [%s]\n", msg1);
printf("msg2 : [%s]\n", msg2);
ptr = strcmp(msg2, msg1);
if(ptr == 0)
printf("msg2 is equal to msg1\n");
printf("Length of msg1 = %d\n",strlen(msg1));
return(0);
}
1
2
3
4
5
6
7
8
9
10
11
12
13
ผลการท างาน
msg1 : [Nanometer]
msg2 : [Nanometer]
msg2 is equal to msg1
Length of msg1 = 9

## หน้า 14
ฟังก์ชันจัดการข้อความ ใน <string.h>
14
ฟังก์ชัน
ค าอธิบาย
char strchr(str, ch)
หาต าแหน่งของตัวอักษรch ในสตริงstr 
แล้วคืนข้อความตั้งแต่ต าแหน่งแรกที่พบch
จนจบ str
char strstr(str1, str2)
หาต าแหน่งของสตริงstr2 ในstr1
แล้วคืนข้อความตั้งแต่ต าแหน่งแรกที่พบstr2 
จนจบ str1
(หน้านี้มีรูปภาพ ข้อความด้านบนไม่รวมเนื้อหาในรูป)

## หน้า 15
ตัวอย่างการใช้ฟังก์ชัน strcmp และ strlen
15
#include <stdio.h>
#include <string.h>
void main (void){   
char str1[30] = "Avengers Help me !!";
char str2[30] = "Help";
char str3[30];
printf("STRSTR : %s\n" , strstr(str1,str2));
printf("STRCHR : %s\n" , strchr(str1,'H'));
printf("STRCPY : %s\n" , strcpy(str3,str2));
printf("STRCMP : %d\n" , strcmp(str3,str2));
printf("STRCAT : %s\n" , strcat(str1,str2));
}
1
2
3
4
5
6
7
8
9
10
11
12
ผลการท างาน
STRSTR : Help me !!
STRCHR : Help me !!
STRCPY : Help
STRCMP : 0
STRCAT : Avengers Help me !!Help

## หน้า 16
อาร์เรย์ของสตริง (Array of Strings)
16
#include <stdio.h>
int main(){
int i;
char subj[][10] = {
"Mechanics", "Drawing", "Material"
};
for(i = 0; i<3;i++)
printf("[%d] = %s\n", i, subj[i]);
return 0;
}
1
2
3
4
5
6
7
8
9
10
ผลการท างาน
[0]
[1]
[2]
[3]
[4]
[5]
[6]
[7]
[8]
[9]
subj[0]
M
e
c
h
a
n
i
c
s
\0
subj[1]
D
r
a
w
i
n
g
\0
0
0
subj[2]
M
a
t
e
r
i
a
l
\0
0
[0] = Mechanics
[1] = Drawing
[2] = Material

## หน้า 17
อาร์เรย์ของสตริง (Array of Strings)
17
#include <stdio.h>
int main(){
int i;
char cs[3][128];
for(i = 0; i< 3;i++){
printf("cs[%d]: ",i);
gets(cs[i]);   
}
for(i = 0; i< 3;i++)
printf("[%d] = %s\n", i, cs[i]);
return 0;
}
1
2
3
4
5
6
7
8
9
10
11
12
ผลการท างาน
[0]: Seoul
[1]: Bangkok
[2]: Tokyo
[0] = Seoul
[1] = Bangkok
[2] = Tokyo

## หน้า 18
18
(หน้านี้มีรูปภาพ ข้อความด้านบนไม่รวมเนื้อหาในรูป)