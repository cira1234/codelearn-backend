## หน้า 1
บทที่ 6
การควบคุมทิศทางการท างานของโปรแกรม 
การท าซ า (Repetition) 
1
(หน้านี้มีรูปภาพ ข้อความด้านบนไม่รวมเนื้อหาในรูป)

## หน้า 2
Welcome to C
ท าไมต้องมีค าสั่งท าซ า
หากเราต้องการเขียนโปรแกรม เพื่อแสดงข้อความเดิม 100 ครั้ง                       
2
printf("Welcome to C\n");
100 ครั้ง
printf("Welcome to C\n");
printf("Welcome to C\n");
printf("Welcome to C\n");
...
printf(“Welcome to C\n”);
การท างานซ า
(หน้านี้มีรูปภาพ ข้อความด้านบนไม่รวมเนื้อหาในรูป)

## หน้า 3
ค าสั่งควบคุมการท าซ าในภาษา C
ค าสั่ง for
ค าสั่ง while
ค าสั่ง do-while
วงรอบ (Loop) หมายถึง ล าดับของค าสั่งใน
ภาษาโปรแกรมที่ท างานซ้ าต่อเนื่อง จนกว่า
เงื่อนไขในการท าซ้ านั้นจะสิ้นสุดลง
3
(หน้านี้มีรูปภาพ ข้อความด้านบนไม่รวมเนื้อหาในรูป)

## หน้า 4
ค าสั่ง for
ประกอบด้วย 3 ส่วน คือ
1.
Index initialization คือการก าหนดค่า
เริ่มต้นให้กับตัวแปรดัชนี (Index) ที่ใช้ควบคุม
การท างานในวงรอบ
2.
Condition คือเงื่อนไขในการเปรียบเทียบ 
หากเป็นจริง จะท าซ้ า (Statement in for 
loop) หากเป็นเท็จ จะออกจากการท าซ้ า
3.
Update index คือ การเปลี่ยนค่าของ
ตัวแปรดัชนี เพื่อให้ผลของการเปรียบเทียบ
เงื่อนไข (Condition) มีแนวโน้มที่จะเป็นเท็จ
จะได้ออกจากการท าซ้ า
4
Statement in
for loop
Index
initialization
Update 
index
Condition
false
true
for (index initialization; 
Condition; Update Index)
Statement ;

## หน้า 5
ไวยากรณ์ของค าสั่ง for
5
for (n = 1; n <= 10; n++) printf("RMUTT\n");
for (n = 10; n >= 1; n--) printf("RMUTT\n");
for (index initialization; Condition; Update Index)
Statement ;
ตัวอย่างค าสั่งแสดงค าว่า RMUTT ทั้งหมด 10 ครั้ง
1
2
for (index initialization; Condition; Update Index){
Statement 1 ;
Statement 2 ;
Statement 3 ;
}

## หน้า 6
ค าสั่ง for
6
การใส่เครื่องหมาย ; หลังเงื่อนไขของค าสั่ง for จะไม่เกิดการท าซ า
เช่น for (n=0; n<=9; n++) ;
สามารถประกาศตัวแปรในส่วนของ index initialization ได้หลายตัว
เช่น 
for (int x=0, y=0; x+y < 30; ++x, y+=5)
printf("%d+%d = %d\n", x, y, x+y);
ส่วนของ condition สามารถใส่นิพจน์การค านวณได้

## หน้า 7
ตัวอย่างการใช้ค าสั่ง for ซ้อนกัน (Nested for)
การแสดงสูตรคูณแม่ 2 ถึงสูตรคูณแม่ 12
2 x 1 = 2
2 x 2 = 4
…
2 x 12 = 24
int m, n;
for (m = 2; m <= 12; m++){
for (n = 1; n <= 12; n++)
printf("%d x %d = %d\n", m, n, m*n);
}
7

## หน้า 8
ตัวอย่างการใช้ค าสั่ง for
การก าหนดค่าให้กับตัวแปรดัชนี  (index) และเปลี่ยนค่าของตัวแปรดัชนีด้วยการรับค่า
อักขระ โดยการใช้ฟังก์ชัน getche
8
ผลการท างาน
123abcq
q has been found
1
2
3
4
5
6
7
8
9
#include <stdio.h>
#include <conio.h>
int main(void) 
{
char c;
for (c=getche(); c!='q'; c=getche());
printf("\n q has been found \n");
return(0);
}
(หน้านี้มีรูปภาพ ข้อความด้านบนไม่รวมเนื้อหาในรูป)

## หน้า 9
ตัวอย่างการใช้ค าสั่ง for
ค าสั่ง continue จะกระโดดไปยังจุด update ของค าสั่ง for 
ค าสั่ง break จะกระโดดออกจาก loop
โดยไม่สนใจค าสั่งต่อไปในส่วนของการท าซ า
ผลการท างาน
1 is odd number
3 is odd number
5 is odd number
7 is odd number
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
int main(void){
int i;
for (i=1; i<100; i++){
if((i%2)== 0) continue;
printf("%d is odd number\n", i);
if (i>5) break;
}
return(0);
}
9
Statement in
for loop
Index
initialization
Update 
index
Condition
false
true

## หน้า 10
ตัวอย่างการใช้ค าสั่ง for
มีลวดหนามยาว 200 เมตร ต้องการล้อมรั วให้มีพื นที่มากที่สุด 
พื นที่นั นมีขนาดเท่าไหร่
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
int x, area, max;
printf("Value of x      Area\n");
max = 0;
for (x=1; x<100; x++){
area = x*(100-x);
printf("%d        %d\n",x,area);
if (area > max) max = area;
}
printf("Maximum area is %d\n", max);
return(0);
}
ผลการท างาน
Value of x      Area
1
99
…
…
10
900
11
979
…
…
50
2500
…
…
58
2436
…
…
99
99
Maximum area is 2500
100-x
x
10

## หน้า 11
ค าสั่ง while
Condition คือ เงื่อนไขในการท าซ้ า
ถ้าผลของการเปรียบเทียบเป็นจริง จึงจะท าค าสั่ง
ในวงรอบ
Statement in While loop คือ ค าสั่งในวงรอบ
ของค าสั่ง while
ก่อนเข้าค าสั่ง while จะต้องก าหนดค่าเริ่มต้น
ให้กับตัวแปรดัชนี (index) ก่อน 
ในที่นี้ คือ ค าสั่ง n 1
ในวงรอบ จะต้องมีค าสั่งเพื่อแก้ไขค่าของตัวแปร
ดัชนี เพื่อให้Condition มีแนวโน้มออกจากวงรอบ
ได้ ในที่นี้ คือ ค าสั่ง n n+1
11
Condition
Statement in
While loop
false
true
n <= 5
n    n+1
false
true
output 
“Hello”
n   1
while (condition)
statement;
(หน้านี้มีรูปภาพ ข้อความด้านบนไม่รวมเนื้อหาในรูป)

## หน้า 12
ตัวอย่างการใช้ค าสั่ง while
12
ผลการท างาน
1. RMUTT
2. RMUTT
3. RMUTT
4. RMUTT
5. RMUTT
n = 1;
while (n <= 5){
printf("%d. RMUTT\n", n);
n++;
}
คำสั่ง while สามารถทำซ้ำได้เพียงหนึ่งคำสั่ง
ถ้าต้องการให้ทำซ้ำมากกว่าหนึ่งคำสั่ง 
ต้องใส่คำสั่งเหล่านั้นไว้ภายใต้เครื่องหมาย { }

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
#include <stdio.h>
int main(void){
int num;
num = 1;
while (num <= 5){ 
printf("%d ", num);
num++;
}
return(0);
}
ผลการท างาน
1 2 3 4 5
13
ตัวอย่างการใช้ค าสั่ง while

## หน้า 14
14
ตัวอย่างการใช้ค าสั่ง while
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
int sum, n;
sum = 0; 
n = 1;
while (n <= 10){
sum = sum+n;
n++;
}
printf("Summation of 1-10 is : %d", sum);
return(0);
}
ผลการท างาน
Summation of 1-10 is 55

## หน้า 15
ตัวอย่างการใช้ค าสั่ง while
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
int sum, data;
sum = 0; 
data = 1;
while (data != 0){
printf("Enter an integer (0 = stop) : ");
scanf("%d",&data);
sum = sum + data;
}
printf("The sum is : %d", sum);
return(0);
}
data
1
3
5
6
0
sum
0
3
8
14
14
3
ผลการท างาน
Enter an integer(0 = stop) : 3
Enter an integer(0 = stop) : 5
Enter an integer(0 = stop) : 6
Enter an integer(0 = stop) : 0
The sum is : 14
15

## หน้า 16
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
float sum, n;
sum = 0; 
n = 1;
while (n > 0){   
sum = sum+n;
n = n-0.1;
}
printf("Summation of 0.1 to 1 is: %f", sum);
return(0);
โปรแกรมหาผลบวกของเลขที่มีทศนิยม 1.0 + 0.9 + 0.8 + … + 0.1
ผลการท างาน
Summation of 1-0.1 is: 5.499999
16
ตัวอย่างการใช้ค าสั่ง while
ถ้าต้องการผลลัพธ์ 5.5 ต้องแก้เป็น %0.1f
⚠️ไม่แนะน าให้ใช้จ านวนจริง เปรียบเทียบกับเลขจ านวนเต็ม เช่น == 0, != 0 เป็นต้น

## หน้า 17
ค าสั่ง do-while
Condition คือ เงื่อนไขในการท าซ้ า
ถ้าผลของการเปรียบเทียบเป็นจริง จะท าค าสั่ง
ในวงรอบถ้าเป็นเท็จ จะออกนอกวงรอบ
Statement in do while loop คือ ค าสั่งใน
วงรอบของค าสั่ง do-while
ก่อนเข้าค าสั่ง do-while จะต้องก าหนดค่าเริ่มต้น
ให้กับตัวแปรดัชนี (index) และในวงรอบ จะต้องมี
ค าสั่งเพื่อแก้ไขค่าของตัวแปรดัชนี เพื่อให้
Condition มีแนวโน้มออกจากวงรอบได้ เหมือน
ค าสั่ง while แต่ค าสั่ง do-while จะท าค าสั่งใน
วงรอบอย่างน้อย 1 ครั้งเสมอ
17
do statement;
while (condition);
Condition
Statement in do 
while loop
false
true
n <= 5
n    n+1
false
true
output 
 Hello 
n   1
(หน้านี้มีรูปภาพ ข้อความด้านบนไม่รวมเนื้อหาในรูป)

## หน้า 18
ตัวอย่างการใช้ค าสั่ง do-while
18
ผลการท างาน
1. RMUTT
2. RMUTT
3. RMUTT
4. RMUTT
5. RMUTT
n = 1;
do{
printf("%d. RMUTT\n", n);
n++;
}while (n <= 5);
คำสั่ง do-while สามารถทำซ้ำได้เพียงหนึ่งคำสั่ง
ถ้าต้องการให้ทำซ้ำมากกว่าหนึ่งคำสั่ง 
ต้องใส่คำสั่งเหล่านั้นไว้ภายใต้เครื่องหมาย { }

## หน้า 19
ตัวอย่างการใช้ค าสั่ง do-while
19
do {
printf("****Menu****\n");
printf(" 1. Show Odd  number\n");
printf(" 2. Show Even number\n");
printf(" 3. Count Up\n");
printf(" 4. Count Down\n");
printf(" Please enter number [1-4] : ");
scanf("%d", &choice);
} while (choice < 0 || choice > 4);
โปรแกรมวนรับเลขจ านวนเต็ม 1 ตัวไปเรื่อย ๆ จนกว่าตัวเลขที่รับเข้าไปนั้น
จะมีค่า 1 ถึง 4 จึงจะออกจากการวนรอบ

## หน้า 20
สรุปการควบคุมการท างานของโปรแกรมแบบท าซ า
หลักในการท าซ า ประกอบด้วยสิ่งส าคัญ 3 สิ่ง คือ
การก าหนดค่าเริ่มต้นให้กับค่าดัชนี (Index)
เงื่อนไข (Condition) ที่จะตัดสินว่า จะให้ท าซ้ าในวงรอบหรือไม่
การปรับค่าดัชนี (Update index) ภายในวงรอบ
i = 1;
while (i <= 5){
printf("RMUTT");
i++;
}
i = 1;
do{
printf("RMUTT");
i++;
}while (i<=5);
for(i=1; i<=5; i++){
printf("RMUTT");
}
20
(หน้านี้มีรูปภาพ ข้อความด้านบนไม่รวมเนื้อหาในรูป)

## หน้า 21
21
(หน้านี้มีรูปภาพ ข้อความด้านบนไม่รวมเนื้อหาในรูป)