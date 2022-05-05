clc

Divsp = zeros(1,45);
Divst = zeros(1,45);
for K=5:45
    % First max returns vector containing maximum
    % value in each column, so we have to call it
    % twice.
    Divsp(K)=max(max(abs(FFp(K)-FFp(K-1))));
    Divst(K)=max(max(abs(FFt(K)-FFt(K-1))));
end

figure()
grid on
plot(Divsp)
title('Div(K) dla interpolacji wielomianowej');
xlabel('K');
ylabel('Div(K)');
saveas(gcf, ['plots/' 'div-poly' '.png']);

figure()
grid on
plot(Divst)
title('Div(K) dla interpolacji trygonometrycznej');
xlabel('K');
ylabel('Div(K)');
saveas(gcf, ['plots/' 'div-trig' '.png']);

function [FF]=FFp(K)
    [x,y,f]=lazik(K);
    [XX,YY]=meshgrid(linspace(0,100,101),linspace(0,100,101));
    [p]=polyfit2d(x,y,f);
    [FF]=polyval2d(XX,YY,p);
end

function [FF]=FFt(K)
    [x,y,f]=lazik(K);
    [XX,YY]=meshgrid(linspace(0,100,101),linspace(0,100,101));
    [p]=trygfit2d(x,y,f);
    [FF]=trygval2d(XX,YY,p);
end