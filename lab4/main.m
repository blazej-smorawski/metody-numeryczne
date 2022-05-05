my_t = @(N) t(N)-5000;
my_v = @(t) v(150000,2000,2700,9.81,t) - 750;
my_z = @(omega) Z(725,omega,8*10^(-5),2) - 75;

[xvect,xdif,fx,it_cnt] = bisect(my_t,[1,60000],10^(-3));
draw(xvect,xdif,fx,it_cnt,"N"," bisect")

[xvect,xdif,fx,it_cnt] = bisect(my_v,[0,50],10^(-12));
draw(xvect,xdif,fx,it_cnt,"v[m per s]"," bisect")

[xvect,xdif,fx,it_cnt] = bisect(my_z,[0,50],10^(-12));
draw(xvect,xdif,fx,it_cnt,"Omega[rad per s]"," bisect")

[xvect,xdif,fx,it_cnt] = secant(my_t,[1,60000],10^(-3));
draw(xvect,xdif,fx,it_cnt,"N"," secant")

[xvect,xdif,fx,it_cnt] = secant(my_v,[0,50],10^(-12));
draw(xvect,xdif,fx,it_cnt,"v[m per s]"," secant")

[xvect,xdif,fx,it_cnt] = secant(my_z,[0,50],10^(-12));
draw(xvect,xdif,fx,it_cnt,"Omega[rad per s]"," secant")

options = optimset('Display','iter');
fzero(@tan,6.0,options)
fzero(@tan,4.5,options)

function draw(xvect,xdif,fx,it_cnt, name, method)
    first_name = name + ' xs';

    figure();
    semilogx(xvect);
    title(name+' as a function of iteration using'+method);
    xlabel('Iterations');
    ylabel(name);
    saveas(gcf, 'plots/'+first_name+method+'.png');

    second_name = name + ' xdif';

    figure();
    plot(xdif);
    title(name + ' difference as a function of iteration using'+method);
    xlabel('Iterations');
    ylabel(name+' difference');
    saveas(gcf, 'plots/'+second_name+method+'.png');
end