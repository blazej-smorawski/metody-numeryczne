function r = gaussseidel(M, b) 
    ress = zeros(1,1000);
    r = ones(size(b));
    D = diag(diag(M));
    L = tril(M) - D;
    U = triu(M) - D;
    index = 1;

    while true 
        resn = norm(residuum(M,r,b));
        ress(index) = resn;
        index = index+1;
        if resn <= 10^(-14)
            break;
        else
            r = -(D+L)\(U*r)+(D+L)\b;
        end
        plot(ress)
        pause(0.01)
    end
end