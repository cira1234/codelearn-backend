## หน้า 1
บทที่ 7
ข้อมูลชนิดแถวล ำดับ Array
1
(หน้านี้มีรูปภาพ ข้อความด้านบนไม่รวมเนื้อหาในรูป)

## หน้า 2
ข้อมูลชนิดแถวล ำดับ (Array)
2
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
int main(void){
int quiz1, quiz2, quiz3, quiz4;
printf("Enter the score:\n");
printf("1st time: "); scanf("%d",&quiz1); 
printf("2nd time: "); scanf("%d",&quiz2);
printf("3rd time: "); scanf("%d",&quiz3);
printf("4th time: "); scanf("%d",&quiz4);
printf("Total score: %d", quiz1 + quiz2 + quiz3 + quiz4);
return(0);
}
Enter the score:
1st time: 5
2nd time: 9
3rd time: 8
4th time: 7
Total score: 29

## หน้า 3
quiz4
quiz3
quiz2
ข้อมูลชนิดแถวล ำดับ (Array)
อ่านว่า อาร์เรย์ คือ กลุ่มของตัวแปรที่เก็บข้อมูลชนิดเดียวกัน
3
quiz1
a[3]
a[2]
a[1]
a[0]
.   [     ] ;
int
a
4
ชนิดข้อมูลของ array
ชื่อตัวแปร array
จ ำนวนข้อมูลใน array

## หน้า 4
Array ในภำษำซี
ข้อมูลแต่ละตัวในอาร์เรย์ เรียกว่า อิลีเมนต์ (Element) หรือเซลล์ (Cell)
แต่ละเซลล์จะใช้ตัวชี้ (Index) ในการอ้างถึงข้อมูลในอาร์เรย์
a[0]
a[1]
a[2]
a[3]
10
20
30
40
ต ำแหน่งของเซลล์แรกในอำร์เรย์ คือ 0 เสมอ
4

## หน้า 5
กำรประกำศตัวแปรArray 1 มิติ
เช่น
int
myarray[20];
จะได้ตัวแปรชื่อ myarray ที่เก็บข้อมูลชนิดจ านวนเต็ม จ านวน 20 เซลล์
ประเภทข้อมูล    ชื่อตัวแปร[จ ำนวนสมำชิก] ;
5

## หน้า 6
ตัวอย่ำงกำรใช้งำน Array 1 มิติ
Array ชื่อ X แต่ละเซลล์เก็บเลขจ านวนเต็ม
ค่าของตัวชี้ ต้องอยู่ในเครื่องหมาย[ ] (วงเล็บเหลี่ยม) เช่น 
X[0] คือ Array X เซลล์ที่ 0 เก็บค่า 18 
X[1] คือ Array X เซลล์ที่ 1 เก็บค่า 20
X[1+3] คือ Array X เซลล์ที่ 4 เก็บค่า 21
X[2] + X[3] คือ ผลบวกของ Array X เซลล์ที่ 2 กับเซลล์ที่ 3
ได้ 35 + 84 = 119
X[0]
X[1]
X[2]
X[3]
X[4]
X[5]
X[6]
X[7]
X
18
20
35
84
21
45
65
74
การเก็บคะแนนของนักศึกษา 8 คน
6

## หน้า 7
ข้อมูลชนิดแถวล ำดับ (Array)
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
int main(void){
int v[4]; 
v[0] = 1;
v[1] = 2;
v[2] = 3;
v[3] = 4;
printf("v[0] = %d\n",v[0]); 
printf("v[1] = %d\n",v[1]);
printf("v[2] = %d\n",v[2]); 
printf("v[3] = %d\n",v[3]); 
return(0);
}
v[0] = 1
v[1] = 2
v[2] = 3
v[3] = 4
ผลการท างาน
7
V[0]
1
V[1]
2
V[2]
3
V[3]
4
ตัวแปร V

## หน้า 8
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
#include <stdio.h>
int main(void) 
{
int quiz[4], i;
int sum = 0; 
printf("Enter the score:\n");
for(i=0; i<4; i++){
printf("Score %d : ",i+1);
scanf("%d",&quiz[i]);
sum += quiz[i];
}
printf("Total score: %d", sum);
return(0);
}
ตัวอย่ำงกำรเข้ำถึงข้อมูลในอำร์เรย์โดยใช้ตัวชี้
8
โปรแกรมหาผลรวมของคะแนนสอบ 4 ครั้ง
quiz[0]
quiz[1]
quiz[2]
quiz[3]
sum
0

## หน้า 9
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
#include <stdio.h>
int main(void) 
{
int quiz[4], i;
int sum = 0; 
printf("Enter the score:\n");
for(i=0; i<4; i++){
printf("Score %d : ",i+1);
scanf("%d",&quiz[i]);
sum += quiz[i];
}
printf("Total score: %d", sum);
return(0);
}
ตัวอย่ำงกำรเข้ำถึงข้อมูลในอำร์เรย์โดยใช้ตัวชี้
9
โปรแกรมหาผลรวมของคะแนนสอบ 4 ครั้ง
quiz[0]
5
quiz[1]
quiz[2]
quiz[3]
Enter the score:
Score 1 : 5
sum
05

## หน้า 10
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
#include <stdio.h>
int main(void) 
{
int quiz[4], i;
int sum = 0; 
printf("Enter the score:\n");
for(i=0; i<4; i++){
printf("Score %d : ",i+1);
scanf("%d",&quiz[i]);
sum += quiz[i];
}
printf("Total score: %d", sum);
return(0);
}
ตัวอย่ำงกำรเข้ำถึงข้อมูลในอำร์เรย์โดยใช้ตัวชี้
10
โปรแกรมหาผลรวมของคะแนนสอบ 4 ครั้ง
quiz[0]
5
quiz[1]
9
quiz[2]
quiz[3]
Enter the score:
Score 1 : 5
Score 2 : 9
sum
5
14

## หน้า 11
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
#include <stdio.h>
int main(void) 
{
int quiz[4], i;
int sum = 0; 
printf("Enter the score:\n");
for(i=0; i<4; i++){
printf("Score %d : ",i+1);
scanf("%d",&quiz[i]);
sum += quiz[i];
}
printf("Total score: %d", sum);
return(0);
}
ตัวอย่ำงกำรเข้ำถึงข้อมูลในอำร์เรย์โดยใช้ตัวชี้
11
โปรแกรมหาผลรวมของคะแนนสอบ 4 ครั้ง
quiz[0]
5
quiz[1]
9
quiz[2]
8
quiz[3]
Enter the score:
Score 1 : 5
Score 2 : 9
Score 3 : 8
sum
14
22

## หน้า 12
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
#include <stdio.h>
int main(void) 
{
int quiz[4], i;
int sum = 0; 
printf("Enter the score:\n");
for(i=0; i<4; i++){
printf("Score %d : ",i+1);
scanf("%d",&quiz[i]);
sum += quiz[i];
}
printf("Total score: %d", sum);
return(0);
}
ตัวอย่ำงกำรเข้ำถึงข้อมูลในอำร์เรย์โดยใช้ตัวชี้
12
โปรแกรมหาผลรวมของคะแนนสอบ 4 ครั้ง
quiz[0]
5
quiz[1]
9
quiz[2]
8
quiz[3]
7
Enter the score:
Score 1 : 5
Score 2 : 9
Score 3 : 8
Score 4 : 7
sum
22
29

## หน้า 13
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
#include <stdio.h>
int main(void) 
{
int quiz[4], i;
int sum = 0; 
printf("Enter the score:\n");
for(i=0; i<4; i++){
printf("Score %d : ",i+1);
scanf("%d",&quiz[i]);
sum += quiz[i];
}
printf("Total score: %d", sum);
return(0);
}
ตัวอย่ำงกำรเข้ำถึงข้อมูลในอำร์เรย์โดยใช้ตัวชี้
13
โปรแกรมหาผลรวมของคะแนนสอบ 4 ครั้ง
quiz[0]
5
quiz[1]
9
quiz[2]
8
quiz[3]
7
Enter the score:
Score 1 : 5
Score 2 : 9
Score 3 : 8
Score 4 : 7
Total score: 29

## หน้า 14
ตัวอย่ำงกำรก ำหนดค่ำเริ่มต้นให้อำร์เรย์
ก าหนดค่า 1 ถึง 7 ให้กับเซลล์ของอาร์เรย์แล้วการรับจ านวนเต็ม7 ค่า
แล้วแสดงผลค่าเฉลี่ย
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
#include <stdio.h>
int main(void){
int i, N = 7;
int a[] = {1,2,3,4,5,6,7};
float sum = 0;
for(i=0; i<N; i++)
sum += a[i];
printf("Mean is %f\n", sum/N);
return(0);
}
14
a[0]
1
a[1]
2
a[2]
3
a[3]
4
a[4]
5
a[5]
6
a[6]
7
กรณีไม่ประกาศขนาดของ Array จะใช้ขนาดตามข้อมูลที่ก าหนดไว้ตั้งแต่ตอนประกาศตัวแปร

## หน้า 15
ตัวอย่ำงกำรก ำหนดค่ำเริ่มต้นให้อำร์เรย์
ก าหนดค่า 1 ถึง 7 ให้กับเซลล์ของอาร์เรย์แล้วการรับจ านวนเต็ม7 ค่า
แล้วแสดงผลค่าเฉลี่ย
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
int main(void){
int i, N = 7;
int a[] = {1,2,3,4,5,6,7};
float sum = 0;
for(i=0; i<N; i++)
sum += a[i];
printf("Mean is %f\n", sum/N);
return(0);
}
15
a[0]
1
a[1]
2
a[2]
3
a[3]
4
a[4]
5
a[5]
6
a[6]
7
sum
0

## หน้า 16
ตัวอย่ำงกำรก ำหนดค่ำเริ่มต้นให้อำร์เรย์
ก าหนดค่า 1 ถึง 7 ให้กับเซลล์ของอาร์เรย์แล้วการรับจ านวนเต็ม7 ค่า
แล้วแสดงผลค่าเฉลี่ย
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
int main(void){
int i, N = 7;
int a[] = {1,2,3,4,5,6,7};
float sum = 0;
for(i=0; i<N; i++)
sum += a[i];
printf("Mean is %f\n", sum/N);
return(0);
}
16
a[0]
1
a[1]
2
a[2]
3
a[3]
4
a[4]
5
a[5]
6
a[6]
7
sum
01

## หน้า 17
ตัวอย่ำงกำรก ำหนดค่ำเริ่มต้นให้อำร์เรย์
ก าหนดค่า 1 ถึง 7 ให้กับเซลล์ของอาร์เรย์แล้วการรับจ านวนเต็ม7 ค่า
แล้วแสดงผลค่าเฉลี่ย
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
int main(void){
int i, N = 7;
int a[] = {1,2,3,4,5,6,7};
float sum = 0;
for(i=0; i<N; i++)
sum += a[i];
printf("Mean is %f\n", sum/N);
return(0);
}
17
a[0]
1
a[1]
2
a[2]
3
a[3]
4
a[4]
5
a[5]
6
a[6]
7
sum
13

## หน้า 18
ตัวอย่ำงกำรก ำหนดค่ำเริ่มต้นให้อำร์เรย์
ก าหนดค่า 1 ถึง 7 ให้กับเซลล์ของอาร์เรย์แล้วการรับจ านวนเต็ม7 ค่า
แล้วแสดงผลค่าเฉลี่ย
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
int main(void){
int i, N = 7;
int a[] = {1,2,3,4,5,6,7};
float sum = 0;
for(i=0; i<N; i++)
sum += a[i];
printf("Mean is %f\n", sum/N);
return(0);
}
18
a[0]
1
a[1]
2
a[2]
3
a[3]
4
a[4]
5
a[5]
6
a[6]
7
sum
36

## หน้า 19
ตัวอย่ำงกำรก ำหนดค่ำเริ่มต้นให้อำร์เรย์
ก าหนดค่า 1 ถึง 7 ให้กับเซลล์ของอาร์เรย์แล้วการรับจ านวนเต็ม7 ค่า
แล้วแสดงผลค่าเฉลี่ย
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
int main(void){
int i, N = 7;
int a[] = {1,2,3,4,5,6,7};
float sum = 0;
for(i=0; i<N; i++)
sum += a[i];
printf("Mean is %f\n", sum/N);
return(0);
}
19
a[0]
1
a[1]
2
a[2]
3
a[3]
4
a[4]
5
a[5]
6
a[6]
7
sum
6
10

## หน้า 20
ตัวอย่ำงกำรก ำหนดค่ำเริ่มต้นให้อำร์เรย์
ก าหนดค่า 1 ถึง 7 ให้กับเซลล์ของอาร์เรย์แล้วการรับจ านวนเต็ม7 ค่า
แล้วแสดงผลค่าเฉลี่ย
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
int main(void){
int i, N = 7;
int a[] = {1,2,3,4,5,6,7};
float sum = 0;
for(i=0; i<N; i++)
sum += a[i];
printf("Mean is %f\n", sum/N);
return(0);
}
20
a[0]
1
a[1]
2
a[2]
3
a[3]
4
a[4]
5
a[5]
6
a[6]
7
sum
10
15

## หน้า 21
ตัวอย่ำงกำรก ำหนดค่ำเริ่มต้นให้อำร์เรย์
ก าหนดค่า 1 ถึง 7 ให้กับเซลล์ของอาร์เรย์แล้วการรับจ านวนเต็ม7 ค่า
แล้วแสดงผลค่าเฉลี่ย
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
int main(void){
int i, N = 7;
int a[] = {1,2,3,4,5,6,7};
float sum = 0;
for(i=0; i<N; i++)
sum += a[i];
printf("Mean is %f\n", sum/N);
return(0);
}
21
a[0]
1
a[1]
2
a[2]
3
a[3]
4
a[4]
5
a[5]
6
a[6]
7
sum
15
21

## หน้า 22
ตัวอย่ำงกำรก ำหนดค่ำเริ่มต้นให้อำร์เรย์
ก าหนดค่า 1 ถึง 7 ให้กับเซลล์ของอาร์เรย์แล้วการรับจ านวนเต็ม7 ค่า
แล้วแสดงผลค่าเฉลี่ย
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
int main(void){
int i, N = 7;
int a[] = {1,2,3,4,5,6,7};
float sum = 0;
for(i=0; i<N; i++)
sum += a[i];
printf("Mean is %f\n", sum/N);
return(0);
}
22
a[0]
1
a[1]
2
a[2]
3
a[3]
4
a[4]
5
a[5]
6
a[6]
7
sum
21
28

## หน้า 23
ตัวอย่ำงกำรก ำหนดค่ำเริ่มต้นให้อำร์เรย์
ก าหนดค่า 1 ถึง 7 ให้กับเซลล์ของอาร์เรย์แล้วการรับจ านวนเต็ม7 ค่า
แล้วแสดงผลค่าเฉลี่ย
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
int main(void){
int i, N = 7;
int a[] = {1,2,3,4,5,6,7};
float sum = 0;
for(i=0; i<N; i++)
sum += a[i];
printf("Mean is %f\n", sum/N);
return(0);
}
23
a[0]
1
a[1]
2
a[2]
3
a[3]
4
a[4]
5
a[5]
6
a[6]
7
sum
28
Mean is 4.000000

## หน้า 24
ตัวอย่าง
24
ก าหนดค่า1 ถึง 10 ให้กับแต่ละเซลล์ของอาร์เรย์ 
แล้วแสดงผลค่าของเลขในเซลล์ยกก าลังสอง
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
#include <stdio.h>
int main(void){
int i, sqrs[10];
for(i=1; i<11; i++)
sqrs[i-1] = i*i;
for(i=0; i<10; i++)
printf("%d\n",sqrs[i]);
return(0);
}
sqrs[0]
sqrs[1]
sqrs[2]
sqrs[3]
sqrs[4]
sqrs[5]
sqrs[6]
sqrs[7]
sqrs[8]
sqrs[9]

## หน้า 25
ตัวอย่าง
25
ก าหนดค่า1 ถึง 10 ให้กับแต่ละเซลล์ของอาร์เรย์ 
แล้วแสดงผลค่าของเลขในเซลล์ยกก าลังสอง
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
#include <stdio.h>
int main(void){
int i, sqrs[10];
for(i=1; i<11; i++)
sqrs[i-1] = i*i;
for(i=0; i<10; i++)
printf("%d\n",sqrs[i]);
return(0);
}
sqrs[0]
1*1
sqrs[1]
2*2
sqrs[2]
3*3
sqrs[3]
4*4
sqrs[4]
5*5
sqrs[5]
6*6
sqrs[6]
7*7
sqrs[7]
8*8
sqrs[8]
9*9
sqrs[9]
10*10

## หน้า 26
ตัวอย่าง
26
ก าหนดค่า1 ถึง 10 ให้กับแต่ละเซลล์ของอาร์เรย์ 
แล้วแสดงผลค่าของเลขในเซลล์ยกก าลังสอง
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
#include <stdio.h>
int main(void){
int i, sqrs[10];
for(i=1; i<11; i++)
sqrs[i-1] = i*i;
for(i=0; i<10; i++)
printf("%d\n",sqrs[i]);
return(0);
}
sqrs[0]
1
sqrs[1]
4
sqrs[2]
9
sqrs[3]
16
sqrs[4]
25
sqrs[5]
36
sqrs[6]
49
sqrs[7]
64
sqrs[8]
81
sqrs[9]
100
1
4
9
16
25
36
49
64
81
100

## หน้า 27
27
ตัวอย่าง
การรับค่า 4 ค่าทางคีย์บอร์ดและแสดงค่าที่รับมาทั้งหมด
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
int main(void){
int i, x[4];
for(i=0; i<4; i++){
printf("x[%d]:",i);
scanf("%d",&x[i]);
}
for(i=0; i<4; i++)
printf("x[%d] =%d\n",i,x[i]);
return(0);
}
x[0]:1
x[1]:2
x[2]:3
x[3]:4

## หน้า 28
28
ตัวอย่าง
การรับค่า 4 ค่าทางคีย์บอร์ดและแสดงค่าที่รับมาทั้งหมด
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
int main(void){
int i, x[4];
for(i=0; i<4; i++){
printf("x[%d]:",i);
scanf("%d",&x[i]);
}
for(i=0; i<4; i++)
printf("x[%d] =%d\n",i,x[i]);
return(0);
}
x[0]:1
x[1]:2
x[2]:3
x[3]:4
x[0] = 1
x[1] = 2
x[2] = 3
x[3] = 4

## หน้า 29
กำรประกำศตัวแปรArray แบบ 2 มิติ
คอลัมน์ที่ 0
คอลัมน์ที่ 1
แถวที่ 0
-19.26
-0.512
แถวที่ 1
11.485
57.96
แถวที่ 2
0.235
762.00
29
m คือ  จ านวนแถวของตัวแปรArray
n
คือ  จ านวนคอลัมน์ของตัวแปรArray
ตัวอย่างการประกาศArray ขนาด 3 แถว 2 คอลัมน์ เพื่อเก็บข้อมูลชนิด float
type
array_name[m][n];
float
real[3][2];
Real[2][1]

## หน้า 30
Array แบบ 3 มิติ
30
เก็บข้อมูลได้หลายแถว หลายคอลัมน์ หลายชั้น
12
58
23
102
6
38
21
44
20
204
41
153
10
15
88
43
3
75
41
78
20
204
47
120
0
125
98
75
5
255
56
56
20
204
47
158
ar[1][1][0]
ar[2][3][2]
ar[2][3][2]
ต ำแหน่งคอลัมน์
ต ำแหน่งแถว
ต ำแหน่งชั้น

## หน้า 31
กำรประกำศและก ำหนดข้อมูลให้กับตัวแปรแบบArray
31
int
number[ ] = {23, -186, 431};
char vowel[5]  = {'a', 'e', 'i', 'o', 'u'};
int
a[5] = {0};
Array 1 มิติ
[0]
23
[1]
-186
[2]
431
number
[0]
a
[1]
e
[2]
i
[3]
o
[4]
u
vowel
[0]
0
[1]
0
[2]
0
[3]
0
[4]
0
a
เซลล์ที่ไม่ได้ก าหนด
ค่าเริ่มต้นให้ตั้งแต่
ตอนประกาศตัวแปร
โปรแกรม Dev C++ 
จะใส่ค่า 0 ให้

## หน้า 32
32
float a[2][2] = {{ 0.0, 1.0 }, { 2.0, 3.0}};
int b[2][2] =   {{ 1 }, { 3 , 4 }};
float matrix[4][4] = {{ 1.0, 0.0, 0.0, 0.0 },
{ 0.0, 1.0, 0.0, 0.0 },
{ 0.0, 0.0, 1.0, 0.0 },
{ 5.0,-3.0, 2.0, 1.0 }};
Array 2 มิติ
[0]
[1]
[0]
0.0
1.0
[1]
2.0
3.0
a
[0]
[1]
[0]
1
0
[1]
3
4
b
[0]
[1]
[2]
[3]
[0]
1.0
0.0
0.0
0.0
[1]
0.0
1.0
0.0
0.0
[2]
0.0
0.0
1.0
0.0
[3]
5.0
-3.0
2.0
1.0
matrix

## หน้า 33
33
int a[2][2] =  { 1, 2, 3, 4 };
int b[3][4] =  { 1, 2, 3, 4, 2, 3, 4, 5, 3, 4, 5, 6 };
int c[ ][4] =  { 1, 2, 3, 4, 2, 3, 4, 5, 3, 4, 5, 6 };
Array 2 มิติ
[0]
[1]
[0]
1
2
[1]
3
4
a
[0]
[1]
[2]
[3]
[0]
1
2
3
4
[1]
2
3
4
5
[2]
3
4
5
6
b
[0]
[1]
[2]
[3]
[0]
1
2
3
4
[1]
2
3
4
5
[2]
3
4
5
6
c

## หน้า 34
ตัวอย่ำงกำรใช้งำนตัวแปรอำร์เรย์ เพื่อหำค่ำต่ ำสุด
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
#include <stdio.h>
int main(void) {
int min, i, N=4;
int a[] = {2,3,0,1};
min = a[0];
for(i=0; i<N; i++) {
printf("a[%d] = %d\n",i,a[i]);
if (a[i] < min) min = a[i];
}
printf("Minimum is %d\n",min);
return(0);
}
34
a[0]
2
a[1]
3
a[2]
0
a[3]
1

## หน้า 35
ตัวอย่ำงกำรใช้งำนตัวแปรอำร์เรย์ เพื่อหำค่ำต่ ำสุด
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
#include <stdio.h>
int main(void) {
int min, i, N=4;
int a[] = {2,3,0,1};
min = a[0];
for(i=0; i<N; i++) {
printf("a[%d] = %d\n",i,a[i]);
if (a[i] < min) min = a[i];
}
printf("Minimum is %d\n",min);
return(0);
}
35
a[0]
2
a[1]
3
a[2]
0
a[3]
1
min
02

## หน้า 36
ตัวอย่ำงกำรใช้งำนตัวแปรอำร์เรย์ เพื่อหำค่ำต่ ำสุด
a[0] = 2
a[1] = 3
a[2] = 0
a[3] = 1
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
#include <stdio.h>
int main(void) {
int min, i, N=4;
int a[] = {2,3,0,1};
min = a[0];
for(i=0; i<N; i++) {
printf("a[%d] = %d\n",i,a[i]);
if (a[i] < min) min = a[i];
}
printf("Minimum is %d\n",min);
return(0);
}
36
a[0]
2
a[1]
3
a[2]
0
a[3]
1
min
2

## หน้า 37
ตัวอย่ำงกำรใช้งำนตัวแปรอำร์เรย์ เพื่อหำค่ำต่ ำสุด
a[0] = 2
a[1] = 3
a[2] = 0
a[3] = 1
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
#include <stdio.h>
int main(void) {
int min, i, N=4;
int a[] = {2,3,0,1};
min = a[0];
for(i=0; i<N; i++) {
printf("a[%d] = %d\n",i,a[i]);
if (a[i] < min) min = a[i];
}
printf("Minimum is %d\n",min);
return(0);
}
37
a[0]
2
a[1]
3
a[2]
0
a[3]
1
min
2

## หน้า 38
ตัวอย่ำงกำรใช้งำนตัวแปรอำร์เรย์ เพื่อหำค่ำต่ ำสุด
a[0] = 2
a[1] = 3
a[2] = 0
a[3] = 1
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
#include <stdio.h>
int main(void) {
int min, i, N=4;
int a[] = {2,3,0,1};
min = a[0];
for(i=0; i<N; i++) {
printf("a[%d] = %d\n",i,a[i]);
if (a[i] < min) min = a[i];
}
printf("Minimum is %d\n",min);
return(0);
}
38
a[0]
2
a[1]
3
a[2]
0
a[3]
1
min
20

## หน้า 39
ตัวอย่ำงกำรใช้งำนตัวแปรอำร์เรย์ เพื่อหำค่ำต่ ำสุด
a[0] = 2
a[1] = 3
a[2] = 0
a[3] = 1
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
#include <stdio.h>
int main(void) {
int min, i, N=4;
int a[] = {2,3,0,1};
min = a[0];
for(i=0; i<N; i++) {
printf("a[%d] = %d\n",i,a[i]);
if (a[i] < min) min = a[i];
}
printf("Minimum is %d\n",min);
return(0);
}
39
a[0]
2
a[1]
3
a[2]
0
a[3]
1
min
0

## หน้า 40
ตัวอย่ำงกำรใช้งำนตัวแปรอำร์เรย์ เพื่อหำค่ำต่ ำสุด
a[0] = 2
a[1] = 3
a[2] = 0
a[3] = 1
Minimum is 0
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
#include <stdio.h>
int main(void) {
int min, i, N=4;
int a[] = {2,3,0,1};
min = a[0];
for(i=0; i<N; i++) {
printf("a[%d] = %d\n",i,a[i]);
if (a[i] < min) min = a[i];
}
printf("Minimum is %d\n",min);
return(0);
}
40
a[0]
2
a[1]
3
a[2]
0
a[3]
1
min
0

## หน้า 41
ตัวอย่ำงกำรใช้งำนตัวแปรอำร์เรย์
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
#include <stdio.h>
int main(void) {
int i, max, min, data[5];
for(i=0; i<5; i++) {
printf("Enter Data[%d] : ",i);
scanf("%d",&data[i]);
}
max = data[0];
min = data[0];
for(i=0; i<5; i++){
printf("Data[%d] = %d\n",i,data[i]);
if (max < data[i]) max = data[i];
if (min > data[i]) min = data[i];
}
printf("Maximum is %d\n",max);
printf("Minimum is %d\n",min);
return(0);
}
41
การรับข้อมูลเข้า แล้วแสดงค่าทั้งหมด พร้อมกับแสดงค่าสูงสุดและค่าต่ าสุด
Enter Data[0] : 2
Enter Data[1] : 9
Enter Data[2] : 8
Enter Data[3] : 4
Enter Data[4] : 7
Data[0] = 2
Data[1] = 9
Data[2] = 8
Data[3] = 4
Data[4] = 7
Maximum is 9
Minimum is 2
ผลการท างาน

## หน้า 42
ตัวอย่ำงกำรใช้งำนตัวแปรอำร์เรย์
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
int matrix[3][3],i,j;
int main(void){
for(i=0;i<3;i++)
for(j=0;j<3;j++){ 
printf("Enter number : ");
scanf("%d",&matrix[i][j]);
}
printf("\n***Matrix***\n");
for(i=0;i<3;i++){
for(j=0;j<3;j++)
printf("%d",matrix[i][j]);
printf("\n");
}
return(0);
}
42
การรับข้อมูลเข้า Matrix ขนาด 3 x 3 แล้วแสดงค่าที่รับเข้าไป
Enter number : 6
Enter number : 8
Enter number : 2
Enter number : 1
Enter number : 4
Enter number : 9
Enter number : 3
Enter number : 7
Enter number : 0
***Matrix***
6  8  2
1  4  9
3  7  0 
ผลการท างาน

## หน้า 43
ตัวอย่ำงกำรบวก Matrix
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
17
18
19
20
21
22
23
24
25
26
#include <stdio.h>
int main(void){
int row, col,
A[3][4] = { 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3 },
B[3][4] = { 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2 };
printf("\n*** Matrix A :\n"); 
for (row=0; row<3; row++) {
for(col=0; col<4; col++)
printf("%2d", A[row][col]);
printf("\n");
}
printf("\n*** Matrix B :\n"); 
for (row=0; row<3; row++) {
for(col=0; col<4; col++)
printf("%2d", B[row][col]);
printf("\n");
}
printf("\n*** Matrix A+B :\n");    
for (row=0; row<3; row++) {
for(col=0; col<4; col++)
printf("%2d", A[row][col]+B[row][col]);
printf("\n");
}
return 0;
}
ผลการท างาน
*** Matrix A :
0 1 2 3
0 1 2 3
0 1 2 3
*** Matrix B :
0 0 0 0
1 1 1 1
2 2 2 2
*** Matrix A+B :
0 1 2 3
1 2 3 4
2 3 4 5

## หน้า 44
44
(หน้านี้มีรูปภาพ ข้อความด้านบนไม่รวมเนื้อหาในรูป)