clc
Ks = [5,15,25,35];

for index=1:size(Ks,2)
    K = Ks(index);
    [x,y,f]=lazik(K);
    
    figure()
    plot(x,y,'-o','linewidth',3)
    kstr = num2str(K);
    title(['Tor ruchu lazika dla K=' kstr]);
    xlabel('x[m]');
    ylabel('y[m]');
    saveas(gcf, ['plots/' 'lazik-' kstr '.png']);

    figure()
    plot3(x,y,f,'o')
    grid on
    title(['Zebrane probki dla K=' kstr]);
    xlabel('x[m]');
    ylabel('y[m]');
    zlabel('f(x,y)')
    saveas(gcf, ['plots/' 'probki-' kstr '.png']);
    
    %grid points
    [XX,YY]=meshgrid(linspace(0,100,101),linspace(0,100,101));

    %polynominal
    [p]=polyfit2d(x,y,f);
    [FF]=polyval2d(XX,YY,p);
    figure()
    surf(XX,YY,FF)
    grid on
    title(['Interpolacja wielomianowa dla K=' kstr]);
    xlabel('x[m]');
    ylabel('y[m]');
    zlabel('f(x,y)')
    saveas(gcf, ['plots/' 'poly-' kstr '.png']);

    %trig
    [p]=trygfit2d(x,y,f);
    [FF]=trygval2d(XX,YY,p);
    figure()
    surf(XX,YY,FF)
    grid on
    title(['Interpolacja trygonometryczna dla K=' kstr]);
    xlabel('x[m]');
    ylabel('y[m]');
    zlabel('f(x,y)')
    saveas(gcf, ['plots/' 'tryg-' kstr '.png']);
end
