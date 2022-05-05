function [xvect,xdif,fx,it_cnt] = secant(fun,range,eps)
    x = (range(1)+range(2))/2;
    it_cnt = 1;
    xvect(it_cnt) = x;
    val = fun(x);
    fx(it_cnt) = val;

    x = range(2);
    it_cnt = it_cnt + 1;
    xvect(it_cnt) = x;
    val = fun(x);
    fx(it_cnt) = val;

    xdif(1)=abs(xvect(2)-xvect(1));
    
    while abs(val)>eps
        it_cnt = it_cnt + 1;
        x = x - fx(it_cnt-1)*( ( xvect(it_cnt-1)-xvect(it_cnt-2) ) / ( fx(it_cnt-1)-fx(it_cnt-2) ) );
        xvect(it_cnt) = x;
        val = fun(x);
        fx(it_cnt) = val;
        xdif(end+1) = abs(xvect(it_cnt)-xvect(it_cnt-1));
    end
end