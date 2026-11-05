## หน้า 1
บทที่ 9
ฟังก์ชันในภาษาซี
Function in C Language
1
(หน้านี้มีรูปภาพ ข้อความด้านบนไม่รวมเนื้อหาในรูป)

## หน้า 2
ท าไมถึงใช้ฟังก์ชัน
int i, sum = 0;
for (i=1; i<=10; i++)
sum +=i;
printf("Sum from 1 to 10 is %d", sum);
sum = 0;
for (i=20; i<=37; i++)
sum +=i;
printf("Sum from 20 to 37 is %d", sum);
หากต้องการเขียนโปรแกรมเพื่อหาค่าผลรวมจาก 1 ถึง 10 และจาก 20 ถึง 37
int sum(int i1, int i2){
int i, sum = 0;
for(i=i1, i<=i2; i++)
sum += i; 
return sum; }
int main(){
printf("Sum from 1 to 10 is %d\n",sum(1,10));
printf("Sum from 20 to 37 is %d",sum(20,37));
}
การเขียนค าสั่ง
โดยไม่เรียกใช้ฟังก์ชัน
การเขียนค าสั่ง
โดยเรียกใช้ฟังก์ชัน
ต้องเขียนคำสั่งเดิม 2 ครั้ง
2
(หน้านี้มีรูปภาพ ข้อความด้านบนไม่รวมเนื้อหาในรูป)

## หน้า 3
ฟังก์ชันคืออะไร
ในการเขียนโปรแกรมคอมพิวเตอร์บางครั้งมีชุดค าสั่งบางชุดที่ถูกเรียกใช้งานบ่อย หาก
ต้องเขียนชุดค าสั่งนั้นบ่อยครั้ง จะท าให้โปรแกรมมีขนาดใหญ่ จึงควรน าเอาชุดค าสั่ง
เหล่านั้นมารวมเป็นฟังก์ชัน
ฟังก์ชัน คือ กลุ่มของค าสั่งที่สามารถถูกเรียกใช้ได้เพื่อท างานเฉพาะอย่าง
ประโยชน์ที่ส าคัญของฟังก์ชันคือช่วยลดความซ้ าซ้อนของโปรแกรม 
อ่านเข้าใจและแก้ไขได้ง่าย
3

## หน้า 4
ฟังก์ชัน (Function)
ฟังก์ชันในภาษาซีแบ่งออกเป็น 2 ประเภท คือ
ฟังก์ชันมาตรฐานของภาษาซี (Standard Library Functions)
ฟังก์ชันที่ภาษาซีจัดเตรียมไว้ให้แล้ว เพียงแต่ต้องทราบก่อนว่าฟังก์ชันนั้นมีการประกาศไว้
ในเฮดเดอร์ไฟล์ใด แล้วเพิ่มบรรทัดค าสั่ง #include <ชื่อเฮดเดอร์ไฟล์>
ตัวอย่างเช่น #include<stdio.h> 
ถ้าไม่มีจะไม่สามารถเรียกใช้ scanf() หรือ printf()
ฟังก์ชันที่ผู้เขียนโปรแกรมสร้างขึ้นเอง (User-defined function)
ฟังก์ชันที่นักพัฒนาโปรแกรมเป็นผู้เขียนขึ้นมาเอง โดยก าหนดชื่อ รูปแบบการรับข้อมูลขา
เข้า รูปแบบการประมวลผลข้อมูล และรูปแบบการคืนค่าข้อมูลขาออก 
ซึ่งสามารถเรียกใช้ซ้ าได้หลายครั้งภายในโปรแกรม
main() ถือเป็นฟังก์ชันชนิดหนึ่งที่เป็นจุดเริ่มต้นท างานของโปรแกรม
กำหนดไว้ที่หัวโปรแกรม
4

## หน้า 5
ฟังก์ชันมาตรฐาน (Standard Function)
Standard Function เป็นฟังก์ชันส าเร็จรูปที่มีมาให้พร้อมกับ Compiler 
โดยเก็บอยู่ในไฟล์ *.h ซึ่งมีรูปแบบดังนี้#include <file.h> 
Library Function ที่ส าคัญ
math.h
ฟังก์ชันการค านวณทางคณิตศาสตร์
string.h
ฟังก์ชันส าหรับข้อความ
ctype.h
ฟังก์ชันส าหรับอักขระ
5

## หน้า 6
ฟังก์ชันการค านวณทางคณิตศาสตร์ ใน math.h
Function
Description
sin(x)
sine ของ x โดยx มีหน่วยเป็นเรเดียน
cos(x)
cosine ของ x โดยx มีหน่วยเป็นเรเดียน
tan(x)
tangent ของ x โดยx มีหน่วยเป็นเรเดียน
sqrt(x)
รากที่สองของ x โดยx>=0
pow(x,y) x ยกก าลัง y
exp(x)
e ยกก าลัง x
log(x)
logarithm ฐาน e ของ x โดยx>=0
log10(x)
logarithm ฐาน 10 ของ x โดยx>=0
abs(x)
ค่าสัมบูรณ์ของ x โดยx เป็นเลขจ านวนเต็ม
fabs(x)
ค่าสัมบูรณ์ของ x โดยx เป็นเลขจ านวนจริง
6
(หน้านี้มีรูปภาพ ข้อความด้านบนไม่รวมเนื้อหาในรูป)

## หน้า 7
ตัวอย่างการใช้ฟังก์ชัน math.h
1
#include <stdio.h>
2
#include <math.h>
3
double x1 = 3.14159, x2 = 2.71828, y;
4
int main(void){
5
y = sin(x1);
6
printf("sin(pi)   = %7.4f\n", y);
7
printf("cos(pi/4) = %7.4f\n", cos(x1/4));
8
printf("tan(pi/6) = %7.4f\n", tan(x1/6));
9
printf("sqrt(2)   = %7.4f\n", sqrt(2));
10
printf("2.5^3     = %7.4f\n", pow(2.5,3));
11
printf("loge(e)   = %7.4f\n", log(x2));
12
printf("log(100)  = %7.4f\n", log10(100));
13
printf("e^3       = %7.4f\n", exp(3));
14
printf("abs(-7)   = %7.4f\n", abs(-7));
15
printf("fabs(-7.0)= %7.4f\n", fabs(-7.0));
16
return(0);
17
}
sin(pi)   =  0.0000
cos(pi/4) =  0.7071
tan(pi/6) =  0.5774
sqrt(2)   =  1.4142
2.5^3     = 15.6250
loge(e)   =  1.0000
log(100)  =  2.0000
e^3       = 20.0855
abs(-7)   =  7.0000
fabs(-7.0)=  7.0000
x = cos() และ y = sin()
7
(หน้านี้มีรูปภาพ ข้อความด้านบนไม่รวมเนื้อหาในรูป)

## หน้า 8
ฟังก์ชันส าหรับข้อความ ใน string.h
Function
Description
strcpy(str1, str2)
คัดลอกข้อความจาก str2 ไปเก็บที่ str1
strcat(str1, str2)
ต่อข้อความใน str1 ด้วย str2
strncat(str1,str2,n)
ต่อข้อความใน str1 ด้วย str2 จ านวน n อักษร
strcmp(str1, str2)
เปรียบเทียบตัวอักษรในข้อความ (case sensitive)                
ถ้า str1 = str2 จะได้ 0
strlen(str)
หาความยาวข้อความ
strlwr(str)
แปลงข้อความภาษาอังกฤษใน str เป็นตัวพิมพ์เล็ก
strupr(str)
แปลงข้อความภาษาอังกฤษใน str เป็นตัวพิมพ์ใหญ่
8
(หน้านี้มีรูปภาพ ข้อความด้านบนไม่รวมเนื้อหาในรูป)

## หน้า 9
ตัวอย่างการใช้ฟังก์ชัน strcpy และ strcat
str1 = [My Birthday 18 August 1991]
str3 = [My Birthday ]
1
#include <stdio.h>
2
#include <string.h>
3
int main(void){
4
char str1[30] = "My Birthday ";
5
char str2[30] = "18 August 1991";
6
char str3[30];
7
strcpy(str3, str1);
8
strcat(str1, str2);
9
printf("str1 = [%s]\n", str1);
10
printf("str3 = [%s]\n", str3);
11
return(0);
12
}
ผลการทำงาน
9

## หน้า 10
ฟังก์ชันส าหรับอักขระ ใน ctype.h
Function
Description
tolower(ch)
เปลี่ยนอักขระเป็นตัวพิมพ์เล็ก
toupper(ch)
เปลี่ยนอักขระเป็นตัวพิมพ์ใหญ่
10
(หน้านี้มีรูปภาพ ข้อความด้านบนไม่รวมเนื้อหาในรูป)

## หน้า 11
ตัวอย่างการใช้ฟังก์ชัน  tolower และ  toupper
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
15
16
17
18
19
#include <stdio.h>
#include <ctype.h>
int main(){
int i;
char string[] = "This Is a String";
i=0;
while(string[i] != '\0'){
string[i] = toupper(string[i]);
i++;
}
printf("%s\n",string);
i=0;
while(string[i] != '\0'){
string[i] = tolower(string[i]);
i++;
}
printf("%s\n",string);
return(0);
}
THIS IS A STRING
this is a string
ผลการท างาน 
11

## หน้า 12
Outline ของฟังก์ชันที่ผู้เขียนโปรแกรมสร้างขึ้นเอง 
ฟังก์ชันที่ผู้เขียนโปรแกรมสร้างขึ้น
โครงสร้างการเรียกใช้ Function 
โครงสร้างของฟังก์ชัน (Structure of Function)
รูปแบบการรับ-ส่งค่าฟังก์ชัน
Pass by Value
Pass by Reference
Function Prototype
Local and Global Variables
การส่งอาร์เรย์เป็นพารามิเตอร์เข้าสู่ฟังก์ชัน
12

## หน้า 13
ฟังก์ชันที่ผู้เขียนโปรแกรมสร้างขึ้น
ฟังก์ชันมาตรฐานที่ภาษาซีเตรียมไว้ให้แล้ว ในบางครั้งอาจไม่ตรงกับความต้องการของ
ผู้เขียนโปรแกรม ภาษาซีจึงเปิดช่องทางให้ผู้เขียนโปรแกรมสามารถสร้างฟังก์ชันขึ้นเอง
ได้ตามต้องการ เราเรียกฟังก์ชันลักษณะนี้ว่า User-Defined Function
13

## หน้า 14
main()
func1()
func2()
{
{
{
func2();
}
func1();
func3()
{
func3();
}
}
}
โครงสร้างการเรียกใช้ฟังก์ชัน
ในการเขียนโปรแกรมด้วยภาษาซีต้องมีฟังก์ชัน main( ) เสมอ  และหากต้องการ
ให้โปรแกรมทำงานฟังก์ชันใด ฟังก์ชัน main( ) จะเป็นผู้เรียกฟังก์ชันนั้นขึ้นมา
ทำงาน ซึ่งในฟังก์ชันนั้นเองก็ยังสามารถเรียกใช้ฟังก์ชันอื่น ๆ ขึ้นมาทำงานได้อีก
ด้วย ดังตัวอย่าง
14

## หน้า 15
โครงสร้างของฟังก์ชัน
โครงสร้างของฟังก์ชัน มีรูปแบบดังนี้
return_type เป็นชนิดของผลลัพธ์ที่ได้จากการทำงานของฟังก์ชัน 
ในกรณีที่ไม่ต้องการส่งค่ากลับให้ใส่ void หากไม่ใส่จะมีค่าเท่ากับ int
function-name คือ ชื่อของฟังก์ชันที่สร้างขึ้นควรตั้งให้สื่อความหมาย
และมีหลักการตั้งชื่อเช่นเดียวกับตัวแปร
return_type function-name(type para-1, type para-2, ... , type para-n)
{
local variable-declarations ;
statement-1 ;
statement-2 ;
...
statement-n ;
return(value) ;
}
15

## หน้า 16
โครงสร้างของฟังก์ชัน
โครงสร้างของฟังก์ชัน มีรูปแบบดังนี้
type para-1, type para-2, ... , type para-n คือ formal parameter(s)
เป็นตัวแปรที่ใช้รับข้อมูลเพื่อนำมาประมวลผลในฟังก์ชัน โดยต้องกำหนดชนิดของ
ตัวแปรไว้ข้างหน้าตัวแปร 
หากมีตัวแปรมากกว่าหนึ่ง ให้คั่นแต่ละตัวด้วยเครื่องหมายจุลภาค แต่หากไม่มี
การรับตัวแปรใดเลย ให้ใส่ void
return_type function-name(type para-1, type para-2, ... , type para-n)
{
local variable-declarations ;
statement-1 ;
statement-2 ;
...
statement-n ;
return(value) ;
}
16

## หน้า 17
โครงสร้างของฟังก์ชัน
โครงสร้างของฟังก์ชัน มีรูปแบบดังนี้
ชุดค าสั่งทั้งหมด จะต้องรวมอยู่ในวงเล็บปีกกา { }
local variable-declarations เป็นการสร้างตัวแปรเพื่อใช้งานภายในฟังก์ชัน
statement-1, statement-2, ... , statement-n ชุดค าสั่งที่รวมอยู่ภายใน
ฟังก์ชัน
return_type function-name(type para-1, type para-2, ... , type para-n)
{
local variable-declarations ;
statement-1 ;
statement-2 ;
...
statement-n ;
return(value) ;
}
17

## หน้า 18
โครงสร้างของฟังก์ชัน
โครงสร้างของฟังก์ชัน มีรูปแบบดังนี้
return(value) เป็นค าสั่งที่ใช้ส าหรับคืนค่าออกจากฟังก์ชัน โดยชนิดของค่าที่คืน
ออกไปต้องเป็นชนิดเดียวกันกับ return_type ที่ประกาศไว้หน้าชื่อของฟังก์ชัน
หากฟังก์ชันไม่มีการคืนค่า ไม่ต้องใช้ค าสั่งนี้ และ return_type ต้องถูกก าหนดให้
เป็น void
return_type function-name(type para-1, type para-2, ... , type para-n)
{
local variable-declarations ;
statement-1 ;
statement-2 ;
...
statement-n ;
return(value) ;
}
18

## หน้า 19
ตัวอย่างโปรแกรมที่ยังไม่ได้สร้างฟังก์ชัน
โปรแกรม
#include <stdio.h>
int main()
{
printf("********************\n");
printf("StarLine Printing\n");
printf("********************\n");
return(0);
}
********************
StarLine Printing
********************
ผลการท างาน
1
2
3
4
5
6
7
8
19

## หน้า 20
ตัวอย่างการสร้างและเรียกใช้ฟังก์ชัน
โปรแกรม
#include <stdio.h>
int main()
{
printf("********************\n");
printf("StarLine Printing\n");
printf("********************\n");
return(0);
}
แทรกช่องว่าง
********************
StarLine Printing
********************
ผลการท างาน
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
20

## หน้า 21
ตัวอย่างการสร้างและเรียกใช้ฟังก์ชัน (ต่อ)
โปรแกรม
#include <stdio.h>
int main()
{
printf("StarLine Printing\n");
return(0);
}
ใส่ชื่อฟังก์ชันเพื่อเรียกใช้งาน
บรรจุค าสั่งเข้าไปใน function
ตั้งชื่อฟังก์ชันขึ้นมาเอง
ใส่ชื่อฟังก์ชันเพื่อเรียกใช้งาน
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
printf("********************\n");
printf("********************\n");
StarLine(
)
StarLine(
)
StarLine(
)
StarLine();
StarLine();
21

## หน้า 22
ตัวอย่าง การเรียกใช้ฟังก์ชันของโปรแกรม
โปรแกรม
#include <stdio.h>
void StarLine(void)
{
printf("********************\n");
}
int main()
{
StarLine();
printf("StarLine Printing\n");
StarLine();
return(0);
}
// ไม่มีการรับ-ส่งค่า จึงใส่ void ทั้งสองต าแหน่ง
// เรียกฟังก์ชัน StarLine (โปรแกรมจะกระโดดเข้าไปท างานใน StarLine)
ผลการท างาน
********************
********************
StarLine Printing
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
ก าหนดขอบเขตฟังก์ชันด้วย {  }
22

## หน้า 23
รูปแบบการรับ-ส่งค่าฟังก์ชัน
ฟังก์ชันสามารถรับ-ส่งค่าได้ 4 รูปแบบดังนี้
1. ไม่มีการรับ-ส่งค่าใด ๆ
ตัวอย่างเช่น
void function_name (void)
หมายเหตุ: ฟังก์ชัน StarLine ที่ผ่านมา ไม่มีการรับ-ส่งค่า (void) StarLine (void)
2. รับค่าเข้าอย่างเดียว  
ตัวอย่างเช่น 
void  function_name (int n)
3. ส่งค่าออกอย่างเดียว
ตัวอย่างเช่น 
float function_name (void)
4. รับและส่งค่า 
ตัวอย่างเช่น 
float function_name (int n)
23

## หน้า 24
ตัวอย่าง ฟังก์ชันที่มีการรับค่าเข้าอย่างเดียว
โปรแกรม
#include <stdio.h>
void StarLine(int n)
{
int i;
for(i=1; i<=n; i++)
printf("*");
printf("\n");
}
int main()
{
StarLine(8);
printf("StarLine Printing\n");
StarLine(17);
return(0);
}
********
StarLine Printing
********************
ผลการท างาน
n เป็น Formal Parameter เป็น local variable 
ใช้เพื่อรับค่าที่ส่งเข้ามาในฟังก์ชันจาก Actual Parameter
ค่า 8 และ 17 เป็น Actual Parameter
เป็นค่าที่ต้องการส่งเข้าไปท างานใน function
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
15
16
24

## หน้า 25
ตัวอย่าง ฟังก์ชันที่มีการส่งค่าออกอย่างเดียว
โปรแกรม
#include <stdio.h>
int get100(void) {
int num, flag = 0;
do {
printf("Please enter score (0-100): ");
scanf("%d",&num);
if(num >= 0 && num <= 100)
flag = 1;
} while(flag == 0);
return num;
}
int main(void) {
int score;
score = get100();
printf("The score entered is %d",score);
return 0;
}
เข้าไปท างานใน get100 
โดยไม่ส่งค่าเข้าไป
get100 คืนค่า num กลับมา ซึ่งเป็นชนิด integer 
ตามที่ระบุไว้ข้างหน้า fucntion
น าค่าที่ได้รับกลับมา ไปก าหนดให้กับ score
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
15
16
17
25
ผลการท างาน
Please enter score (0-100):-5
Please enter score (0-100):99
The score entered is 99

## หน้า 26
ตัวอย่าง ฟังก์ชันที่มีการรับและส่งค่ากลับ
โปรแกรม
#include <stdio.h>
float FindArea(float radius)
{
return(3.14*radius*radius);
}
int main(void)
{
float radius, area;
printf("Enter Radius: ");
scanf("%f", &radius);
area = FindArea(radius);
printf("Area is %0.2f\n", area);
return(0);
}
Enter Radius: 5
Area is 78.50
ผลการท างาน
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
เข้าไปท างานใน FindArea โดยส่งค่า Actual 
Parameter ไปเก็บไว้ใน Formal Parameter
(สามารถตั้งชื่อ Actual Parameter เหมือนกับ 
Formal Parameter ได้ เพราะคนละฟังก์ชัน
กัน)
FindArea คืนค่า ที่ค านวณได้กลับมา
น าค่าที่ได้รับกลับมา ไปก าหนดให้กับ area
26

## หน้า 27
การส่งข้อมูลเข้าสู่ฟังก์ชัน
ฟังก์ชันที่มีการรับค่า มี 2 แบบ ตามลักษณะของพารามิเตอร์ที่ส่งให้ฟังก์ชัน
1. Pass by Value 
เป็นการส าเนาค่าของ Actual parameter ให้ Formal Parameter 
หากค่าของ Formal Parameter เปลี่ยนไป จะไม่มีผลกับค่าของ Actual 
Parameter
2. Pass by Reference
เป็นการส่งต าแหน่งหน่วยความจ าของ Actual parameter  ให้กับ Formal 
Parameter ท าให้ Formal Parameter กับ Actual Parameter เสมือนเป็น
ตัวแปรเดียวกัน
หากค่าของ Formal Parameter เปลี่ยนไป ค่าของ Actual Parameter 
จะเปลี่ยนด้วย
27

## หน้า 28
ตัวอย่าง Pass by Value
#include <stdio.h>
float FindArea(float radius)
{
return(3.14*radius*radius);
}
int main(void)
{
float radius, area;
printf("Enter Radius: ");
scanf("%f", &radius);
area = FindArea(radius);
printf("Area is %0.2f\n", area);
return(0);
}
Enter Radius: 5
Area is 78.50
ผลการท างาน
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
เข้าไปท างานใน FindArea
โดยส่งค่า Actual Parameter 
ไปเก็บไว้ใน Formal Parameter
FindArea คืนค่า ที่ค านวณได้กลับมา
น าค่าที่ได้รับกลับมา ไปก าหนดให้กับ area
28

## หน้า 29
Pass by Reference
Pass by Reference เป็นการส่งต าแหน่งหน่วยความจ าของ Actual Parameter  
ให้กับ Formal Parameter ท าให้ Formal Parameter เสมือนเป็นตัวแปรเดียวกัน
กับ Actual Parameter
องค์ความรู้พื้นฐานที่จ าเป็นต่อการท าความเข้าใจ Pass by Reference
ต าแหน่งของหน่วยความจ า (Memory Address)
ตัวแปร Pointer
29

## หน้า 30
ต าแหน่งหน่วยความจ า (Memory Address)
#2020
a
ตัวแปรแต่ละตัวจะถูกสร้างขึ้นใน RAM และมีหมายเลขตำแหน่งใน RAM เรียกว่า 
“Address” เมื่อเรากำหนดค่าให้กับตัวแปร ค่านั้นจะถูกเก็บไว้ใน RAM ที่ Address 
ของตัวแปรนั้น ดังตัวอย่าง
int a;
a = 19;
สร้างกล่องชื่อว่า a เพื่อเก็บข้อมูลชนิด integer 
และกล่องนี้อยู่ ณ Address #2020
นำค่า 19 ไปเก็บไว้ในกล่องชื่อว่า a
ซึ่งก็คือ การนำค่า 19 ไปเก็บไว้ใน Address 
#2020 ของ RAM
int b = 55;
#1974
b
สำเนาค่าในกล่อง b ไปเก็บไว้ในกล่อง a
ซึ่งก็คือการสำเนาค่าใน RAM Address #1974 
ไปเก็บไว้ใน RAM Address #2020
a = b;
30
สร้างกล่องชื่อว่า b เพื่อเก็บข้อมูลชนิด integer 
และกล่องนี้อยู่ ณ Address #1974

## หน้า 31
Pass by Reference (ต่อ)
เป็นตัวแปรที่ใช้เก็บ Address (ตำแหน่งในหน่วยความจำ) ของตัวแปร 
ซึ่งแตกต่างกับตัวแปรชนิดพื้นฐานที่สร้างขึ้นมาเพื่อเก็บข้อมูล เช่น จำนวนเต็ม จำนวนจริงฯลฯ
ตัวแปร Pointer
a
#1357
#2468
b
int a = 20;
int *b;
สร้างตัวแปร a เพื่อเก็บข้อมูล integer พร้อมกับ
กำหนดค่า 20 เข้าไป และตัวแปรนี้อยู่ใน RAM
Address #1357
เป็นการสร้าง pointer ชื่อว่า b อยู่ใน Address 
#2468
b = &a;
กำหนดค่า Address ของ a (#1357) ให้กับ 
pointer b
ดังนั้น เมื่อเข้าถึงข้อมูลใน b จะพบ Address ของ a (#1357) และด้วย 
address นี้เองท าให้เราสามารถเข้าถึงข้อมูลใน a (20) ได้
31

## หน้า 32
0x7ffcfc961998
ตัวอย่าง Pass by Reference
a
0x7ffcfc961998
0x7ffcfc961990
b
#include <stdio.h>
int main(void) {
int a=20;
int *b;   //การสร้างตัวแปร pointer ชื่อb    
printf("a ถูกจองอยู่ใน RAM Address ที่ %p และเก็บค่า %d ไว้แล้ว\n",&a,a);
b = &a;
printf("pointer b ถูกจองใน RAM Address ที่%p และเก็บค่า %p\n",&b,b);
printf("ซึ่งเป็น Address ของ a\n");
*b = 55;  // *b หมายถึง ข้อมูลของตัวแปร ณ Address ที่ b เก็บไว้
printf("ข้อมูลในตัวแปร a ถูกเปลี่ยนเป็น %d (ผ่านทาง pointer b)\n",a);
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
a ถูกจองอยู่ใน RAM Address ที่ 0x7ffcfc961998 และเก็บค่า 20 ไว้แล้ว
ผลการท างาน
pointer b ถูกจองใน RAM Address ที่ 0x7ffcfc961990 และเก็บค่า 0x7ffcfc961998
ซึ่งเป็น Address ของ a
ข้อมูลในตัวแปร a ถูกเปลี่ยนเป็น 55 (ผ่านทาง pointer b)
%p คือ format string ที่ใช้
แสดงค่า Address ของตัวแปร
32
&ชื่อตัวแปร = Address ของตัวแปร
var-type *var-name = การสร้างตัว
แปรชนิด pointer
ชื่อpointer = Address ที่เก็บอยู่ใน 
pointer
*ชื่อpointer = ค่าของตัวแปร 
ณ Address ที่เก็บไว้ใน pointer

## หน้า 33
ตัวอย่าง Pass by Reference
#include <stdio.h>
void NumChange(int *number2){
printf("Before change : %d\n",*number2);
*number2 += 5;
printf("After change  : %d\n",*number2);
}
int main(void){
int number = 15;
NumChange(&number);
printf("After entering the function : %d\n",number);
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
number
0x7ffcfc961998
0x7ffcfc961990
number2
Before change : 15
ผลการท างาน
After change  : 20
After entering the function : 20
การท า Pass by Reference 
ไม่สามารถให้ Actual Parameter เป็นค่าคงที่ได้ 
เพราะค่าคงที่ไม่มีการจองหน่วยความจ า 
จึงไม่มี Address ส่งให้ Formal Parameter 
ซึ่งเป็นตัวแปรชนิด Pointer
33

## หน้า 34
Function Prototype
ฟังก์ชันสามารถมองเห็นและเรียกใช้งานฟังก์ชันที่อยู่บรรทัดบนกว่าได้
เนื่องจากฟังก์ชันส่วนบนนั้นได้ผ่านการแปลโดยCompiler เรียบร้อยแล้ว
#include <stdio.h>
void StarLine(void)
{...}
void NumChange(int number)
{...}
float FindArea(float radius)
{...}
int main()
{...}
ยังไม่รู้จัก NumChange and FindArea จึงเรียกใช้สองฟังก์ชันนี้ไม่ได้
รู้จัก StarLine แล้วจึงเรียกใช้งานได้แต่ยังไม่รู้จักFindArea
รู้จัก StarLine และ NumChange แล้วจึงเรียกใช้สองฟังก์ชันนี้ได้
รู้จักทั้ง 3 ฟังก์ชันแล้วจึงเรียกใช้ทั้ง 3 ฟังก์ชันได้
34
หากฟังก์ชันที่อยู่ด้านบนต้องการเรียกฟังก์ชันที่อยู่ด้านล่าง จำเป็นต้องประกาศ 
Prototype ของฟังก์ชันทั้งหมดไว้ก่อน

## หน้า 35
Function Prototype (ต่อ)
Prototype เปรียบเสมือนโครงสร้างโดยคร่าวของ Function 
ซึ่งประกอบไปด้วย var_type, Function Name และ Parameter Set
ตำแหน่งของPrototype ควรอยู่บริเวณต้นโปรแกรม (ถัดจาก Preprocessor 
Directives) หรือบริเวณต้นของฟังก์ชัน main 
• เพื่อที่ Compiler จะได้รู้จักชื่อและโครงสร้าง (return_type and parameter)
ของฟังก์ชัน 
• และสามารถแปลคำสั่งที่มีการเรียกใช้ฟังก์ชันที่สร้างไว้ในบรรทัดล่างกว่าได้ 
(เพราะได้รู้จักโครงสร้างโดยคร่าวที่ประกาศไว้ก่อนหน้านี้แล้ว)
35

## หน้า 36
Function Prototype (ต่อ)
ตัวอย่างโครงสร้างโปรแกรมที่มีการสร้าง Prototype
#include <stdio.h>
void StarLine(void);
void NumChange(int number);
float FindArea(float radius);
int main(void)
{...}
void StarLine(void)
{...}
void NumChange(int number)
{...}
float FindArea(float radius)
{...}
Function Prototypes
Function
ฟังก์ชัน StarLine สามารถเรียกใช้ฟังก์ชัน NumChange และ FindArea ได้ 
เนื่องจาก Compiler รู้จักชื่อ, ข้อมูลเข้า (Formal Parameter), และข้อมูลออก
(Return Type) ของฟังก์ชันตั้งแต่ตอนสร้าง Prototype ที่ต้นโปรแกรม
36

## หน้า 37
Function Prototype (ต่อ)
ผลการท างาน
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
#include <stdio.h>
void StarLine(void);
// Prototype of StarLine Function
int main()
{
StarLine();
// Function Call
printf("StarLine Printing\n");
StarLine();
// Function Call
return(0);
}
void StarLine(void)
// StarLine Function
{
printf("********************\n");
}
********************
StarLine Printing
********************
37

## หน้า 38
Function Prototype (ต่อ)
ผลการท างาน
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
15
#include <stdio.h>
int ADD_AB(int A, int B);
// Function Prototype
int main()
{
int A=2, B=7, C;
C = ADD_AB(A,B);
// Function Call
printf("Answer is %d",C);
return(0);
}
int ADD_AB(int A, int B)
// Function
{
int x;
x = A+B;
return(x);
}
Answer is 9
38

## หน้า 39
ชนิดของตัวแปรแยกตามขอบเขตการท างาน
ตัวแปรชนิดโกลบอล (Global Variable) เป็นตัวแปรที่ประกาศไว้นอกฟังก์ชัน 
แนะนำให้ประกาศไว้ตอนต้นของโปรแกรม จะได้เรียกใช้งานได้ทุกที่ 
และทุกฟังก์ชันในโปรแกรม
ตัวแปรชนิดโลคอล (Local Variable) เป็นตัวแปรที่ประกาศไว้ในฟังก์ชัน 
และมีผลแค่ภายในฟังก์ชันเท่านั้น (ตัวแปรจะถูกทำลายเมื่อออกจากฟังก์ชัน) 
หากมีชื่อซ้ำกับ Global variable จะถือว่าเป็นคนละตัวแปรกัน 
39

## หน้า 40
40
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
#include <stdio.h>
int num = 19;
void increase( ){
num = num + 5;
}
void main( ){ 
printf("num = %d\n", num);
increase();
printf("num = %d\n", num);
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
#include <stdio.h>
void increase( ){ 
int num = 2;
num = num + 5;
}
void main( ){ 
int num = 19;
printf("num = %d\n", num);
increase();
printf("num = %d\n", num);
}
Global variable
ชนิดของตัวแปรแยกตามขอบเขตการท างาน (ต่อ)
40
Local variable
num = 19
num = 24
ผลลัพธ์
num = 19
num = 19
ผลลัพธ์
19+5 = 24
2+5 = 7

## หน้า 41
การส่งอาร์เรย์เป็นพารามิเตอร์ให้กับฟังก์ชัน
เป็นการส่งข้อมูลเข้าฟังก์ชันแบบ Pass by Reference เนื่องจาก
• ไม่ต้องจองหน่วยความจำอีก 1 ชุดที่มีขนาดเท่ากับ Array เพื่อรับข้อมูลจาก
Actual Parameter ทำให้ประหยัดพื้นที่หน่วยความจำ
• ลดการประมวลผล ในการสำเนาข้อมูลจาก Actual สู่ Formal Parameter
• ลดการประมวลผล ในการส่งค่า Array ทั้งชุดออกจากฟังก์ชัน 
(กรณีที่ต้องการส่ง Array กลับมาประมวลผลต่อ)
41
mat[4]
mat[3]
mat[2]
mat[1]
mat[0]
v[4]
v[3]
v[2]
v[1]
v[0]

## หน้า 42
ตัวอย่าง ฟังก์ชันที่รับค่าเป็นอาร์เรย์
#include <stdio.h>
void Dollar(float baht[], int num)
{
int i;
printf("Before changing : %.2f\n", baht[0]);
for(i=0; i<num; i++)
baht[i] *= 40.0;
printf("After changing  : %.2f\n", baht[0]);
}
int main()
{
float money[3] = {200.0, 400.0, 600.0};
Dollar(money, 3);
printf("After entering function: %.2f\n", money[0]);
return(0);
}
Before changing : 200.00
After changing  : 8000.00
After entering function: 8000.00
ผลการท างาน
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
15
16
อ้างแค่ชื่อ Array ในตำแหน่ง 
Actual Parameter 
พร้อมส่งขนาดของ Array
• เหมือนการประกาศ Array
• สามารถไม่ระบุขนาดได้
เฉพาะมิติแรกเท่านั้น
42

## หน้า 43
ตัวอย่าง ฟังก์ชันที่รับค่าเป็นอาร์เรย์
43
43
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
15
16
#include <stdio.h>
int max_of(int v[],int n);
int main(){
int mat[5] = {45,36,72,90,100};
int max_m;
max_m = max_of(mat,5);
printf("max value of score %d",max_m);
}
int max_of(int v[],int n) {
int max = v[0]; 
for (int i = 1; i< n; i++){
if(v[i]> max)
max = v[i];}
return max;
}
max value of score 100
ผลการท างาน

## หน้า 44
ตัวอย่าง ฟังก์ชันที่รับค่าเป็นอาร์เรย์
#include <stdio.h>
void printArray(int [][3]);
int main(void) {
int array1[2][3] = {{1,2,3},{4,5,6}},
array2[2][3] = {1,2,3,4,5},
array3[2][3] = {{1,2},{4}};
printf("Value in array1 by row are:\n");
printArray(array1);
printf("Value in array2 by row are:\n");
printArray(array2);
printf("Value in array3 by row are:\n");
printArray(array3);
return 0;
}
void printArray(int a[][3]) {
int i,j;
for (i=0; i<2; i++) {
for (j=0; j<3; j++) 
printf("%d ",a[i][j]);
printf("\n");
}
}
Value in array1 by row are:
1 2 3 
4 5 6 
Value in array2 by row are:
1 2 3 
4 5 0 
Value in array3 by row are:
1 2 0 
4 0 0 
ผลการท างาน
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
15
16
17
18
19
20
21
22
44

## หน้า 45
ตัวอย่าง การส่งผ่านค่าสตริงระหว่างฟังก์ชัน
#include <stdio.h>
void greeting(char [ ]);
void main (void){
char string[20]; 
printf("What is your name => ");
gets(string);
greeting(string);
}
void greeting(char name[]){    
printf("Hello there %s!" , name );
} 
What is your name => Harry Potter
Hello there Harry Potter!
ผลการท างาน
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
มีหลักการเหมือนการส่ง Array เข้าสู่ฟังก์ชัน 
เนื่องจาก String เป็น Array of Character
45

## หน้า 46
ตัวอย่าง การส่งผ่านค่าสตริงระหว่างฟังก์ชัน
#include <stdio.h>
void greeting(char [] );
void main (void)
{   char string[20];
greeting(string);
printf("You are scaring me: %s!\n" , string);
}
void greeting(char name[]){
printf("Enter your first name => ");
gets(name);  
}
Enter your first name => Voldemort
You are scaring me: Voldemort!
ผลการท างาน
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
เปลี่ยนแปลงข้อมูลในฟังก์ชัน 
greeting โดยการรับข้อมูลจาก
ฟังก์ชัน gets
ข้อมูลใน string เปลี่ยนตาม
name ในฟังก์ชัน greeting
46

## หน้า 47
สรุปการส่งผ่านค่าอาร์เรย์และสตริงระหว่างฟังก์ชัน 
Formal Parameter ที่รับค่าอาร์เรย์หรือสตริง สามารถไม่ระบุขนาดของอาร์เรย์มิติ
แรก แต่มิติที่เหลือจำเป็นต้องระบุ
void Dollar(float baht[], int num) {...}
void modifyArray(int b[], int size) {...}
void printArray(int a[][3]) {...}
void greeting(char name[]) {...}
47

## หน้า 48
48
(หน้านี้มีรูปภาพ ข้อความด้านบนไม่รวมเนื้อหาในรูป)