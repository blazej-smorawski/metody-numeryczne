function r = gen_and_solve(N,density)
    Edges=generate_network(N, density);
    
    m = size(Edges,2);
    d = 0.85;
    diagA = zeros(1,N);
    I = speye(N);
    B = sparse(Edges(1,:),Edges(2,:),ones(1,m));
    b = (1-d)/N * ones(N,1);
    
    for index = 1:N
        diagA(index) = 1/sum(B(:,index));
    end
    
    A = sparse(1:N,1:N,diagA,N,N);
    
    M = I-d*B*A;
    r = M\b;
end