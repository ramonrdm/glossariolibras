// Compilar com -pthread: ex. gcc compete.c -pthread -o compete

#include <pthread.h> 
#include <stdio.h> 

#define NUM_REPETICOES  1000000

pthread_t tid0, tid1;  
long x=0; 
 
void *t0(){  
  long i; 
  for (i = 0; i < NUM_REPETICOES; i++){
    x = x + 5;
  }
  printf("t2 finalizou\n");
}
 
void *t1(){
  long i ; 
  for (i = 0; i < NUM_REPETICOES; i++){ 
    x = x - 5; 
  } 
  printf("t1 finalizou\n"); 
}

int main(){ 
   pthread_create(&tid0, NULL, t0, NULL) ; 
   pthread_create(&tid1, NULL, t1, NULL) ; 
   pthread_join(tid0,NULL);  
   pthread_join(tid1,NULL);  
   printf("O valor de x eh: %ld\n",x); 
   return 0;
}
