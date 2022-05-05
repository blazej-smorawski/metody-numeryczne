function v = v(m,u,q,g,t)
    v = u*log( m/(m-q*t) ) - g*t;
end