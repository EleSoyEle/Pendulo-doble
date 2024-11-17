#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <unistd.h>

float g = 9.8;

// Definimos las variables globales
float m1 = 1;
float m2 = 1;
float l1 = 1;
float l2 = 1;

//Condiciones iniciales del pendulo doble
float theta;
float dtheta = 0;

float phi;
float dphi = 0;

float ti = 0;

//Vamos a deinir la función que calcula las respectivas segundas derivadas
float* d2y(float theta_,float phi_,float dtheta_,float dphi_,float t_){
    float dif_angs = theta_-phi_;
    float cos_dif = cos(dif_angs);
    float sin_dif = sin(dif_angs);
    float A = m2*pow(l2,2);
    float B = m2*l1*l2*cos_dif;
    float C = (m1+m2)*pow(l1,2);

    float beta_1 = m2*l1*l2*pow(dtheta_,2)*sin_dif-m2*g*l2*sin(phi_);
    float beta_2 = -m2*l1*l2*pow(dphi_,2)*sin_dif-(m1+m2)*g*l1*sin(theta_);

    float deter = A*C-pow(B,2);
    float d2phi = (beta_1*C-B*beta_2)/deter;
    float d2theta = (A*beta_2-beta_1*B)/deter;
    
    float* ptr = (float*)calloc(2,sizeof(float));
    ptr[0] = d2theta;
    ptr[1] = d2phi;
    return ptr;
}

float* d1y(float theta_,float phi_,float dtheta_,float dphi_,float t_){
    float* ptr = (float*)calloc(2,sizeof(float));
    ptr[0] = dtheta_;
    ptr[1] = dphi_;
    return ptr;
}
float* calc_rk_gen_step(
    float theta_,float phi_,float dtheta_,float dphi_,
    float* (*f)(float,float,float,float,float),
    float* (*g)(float,float,float,float,float),
    float h,float t_){
    float* k1x = f(theta_,phi_,dtheta_,dphi_,t_);
    float* k1v = g(theta_,phi_,dtheta_,dphi_,t_);
    float* k2x = f(theta_+h*k1x[0]/2,phi_+h*k1x[1]/2,dtheta_+h*k1v[0]/2,dphi_+h*k1v[1]/2,t_+h/2);
    float* k2v = g(theta_+h*k1x[0]/2,phi_+h*k1x[1]/2,dtheta_+h*k1v[0]/2,dphi_+h*k1v[1]/2,t_+h/2);
    float* k3x = f(theta_+h*k2x[0]/2,phi_+h*k2x[1]/2,dtheta_+h*k2v[0]/2,dphi_+h*k2v[1]/2,t_+h/2);
    float* k3v = g(theta_+h*k2x[0]/2,phi_+h*k2x[1]/2,dtheta_+h*k2v[0]/2,dphi_+h*k2v[1]/2,t_+h/2);
    float* k4x = f(theta_+h*k3x[0],phi_+h*k3x[1],dtheta_+h*k3v[0],dphi_+h*k3v[1],t_+h);
    float* k4v = g(theta_+h*k3x[0],phi_+h*k3x[1],dtheta_+h*k3v[0],dphi_+h*k3v[1],t_+h);

    float* ptr = (float*)calloc(5,sizeof(float));
    ptr[0] = theta_ + h*(k1x[0]+2*k2x[0]+2*k3x[0]+k4x[0])/6;
    ptr[1] = phi_ + h*(k1x[1]+2*k2x[1]+2*k3x[1]+k4x[1])/6;
    ptr[2] = dtheta_ + h*(k1v[0]+2*k2v[0]+2*k3v[0]+k4v[0])/6;
    ptr[3] = dphi_ + h*(k1v[1]+2*k2v[1]+2*k3v[1]+k4v[1])/6;
    ptr[4] = t_+h;
    return ptr;

}


int main(){
    FILE *fptr;
    FILE *ptr_info;
    
    ptr_info = fopen("info.txt","w");
    fprintf(ptr_info,"%f,%f",l1,l2);
    fclose(ptr_info);

    printf("Ingresa el angulo theta inicial: ");
    scanf("%f",&theta);
    printf("Ingresa el angulo phi inicial: ");
    scanf("%f",&phi);

    fptr = fopen("datos.txt","w");
    int steps;
    printf("Ingresa el número de iteraciónes: ");
    scanf("%d",&steps);


    float h=0.01;
    for(int step=0;step<steps;step++){
        float* rk_s = calc_rk_gen_step(theta,phi,dtheta,dphi,d1y,d2y,h,ti);
        theta = rk_s[0];
        phi = rk_s[1];
        dtheta = rk_s[2];
        dphi = rk_s[3];
        ti = rk_s[4];

        for(int i=0;i<5;i++){
            fprintf(fptr,"%f ",rk_s[i]);
        }
        fprintf(fptr,"\n");
    }
    fclose(fptr);
    system("python3 animation.py");
    return 0;
}