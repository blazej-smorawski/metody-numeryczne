function [xvect,xdif,fx,it_cnt] = bisect(fun,range,eps)
    a = range(1);
    b = range(2);
    x = (a+b)/2;
    it_cnt = 1;
    xvect(it_cnt) = x;
    val = fun(x);
    fx(it_cnt) = val;
    xdif = [];

    while abs(val)>eps
        it_cnt = it_cnt + 1;
        if( sign(val)==sign(fun(a)) )
            a = x;
        else
            b = x;
        end
        x = (a+b)/2; 
        xvect(it_cnt) = x;
        val = fun(x);
        fx(it_cnt) = val;
        xdif(end+1) = abs(xvect(it_cnt)-xvect(it_cnt-1));
    end
end