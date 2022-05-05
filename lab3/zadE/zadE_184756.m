clear
% Przygotowujemy tablice pomocnicze
Ns = [500,1000,3000,6000,12000];
times = zeros(size(Ns));
tries = zeros(size(Ns));
ress = zeros(1,1000);

for x = 1:size(Ns,2)
    % Wektor wynikowy
    r = ones(Ns(x),1);

    [M,b]=gen_data(Ns(x), 10, 0.85);
    
    tic
    % Rozwiązujemy układ równań metodą jacobiego
    D = diag(diag(M));
    L = tril(M) - D;
    U = triu(M) - D;
    tnum = 1;
    
    while true 
        resn = norm(residuum(M,r,b));
        ress(tnum) = resn;
        tnum = tnum + 1;
        if resn <= 10^(-14)
            break;
        else
            r = -(D\((L+U)*r))+(D\b);
        end
    end
    % Wykres błędu rezydualnego
    figure(x)
    semilogy(ress);
    xlabel("Numer iteracji")
    ylabel("Błąd rezydualny")
    title(sprintf("Norma residuum dla układu równań dla N = %d", Ns(x)))
    name = sprintf("zadE/zadE_184756_%d",x);
    print(name,'-dpng','-r300')

    times(x) = toc;
    tries(x) = tnum;
end

% Wykres czasu
figure(size(Ns,2))
plot(Ns,times)
xlabel("N - liczba stron")
ylabel("Czas rozwiązania")
title("Czasy rozwiązywania układów równań metodą Jacobiego w funkcji N")
print("zadE/zadE_184756_czas",'-dpng','-r300')

% Wykres liczby iteracji
figure(size(Ns,2)+1)
plot(Ns,tries)
xlabel("N - liczba stron")
ylabel("Liczba iteracji algorytmu Jacobiego")
title("Liczba iteracji potrzebna do rozwiązania metodą Jacobiego")
print("zadE/zadE_184756_iteracje",'-dpng','-r300')