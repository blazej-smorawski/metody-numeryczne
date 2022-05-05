% Wyczyszczenie i wczytanie danych
clear
load("zadG/Dane_Filtr_Dielektryczny_lab3_MN.mat")

tic
M\b;
toc

% Obie metody są rozbieżne i nie dają nam dobrych wyników
tic
gaussseidel(M,b)
toc

tic
jacobi(M,b)
toc
