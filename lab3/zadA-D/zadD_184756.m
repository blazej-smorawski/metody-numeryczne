clear
Ns = [500,1000,3000,6000,12000];
times = zeros(size(Ns));
density = 10;

for x = 1:size(Ns,2)
    tic
    gen_and_solve(Ns(x),density);
    times(x) = toc;
end

hold on
plot(Ns,times)
xlabel("N - liczba stron")
ylabel("Czas rozwiązania metodą bezpośrednią [s]")
title("Czasy rozwiązywania układów równań metodą bezpośrednią w funkcji N")
print("zadA-D/zadD_184756",'-dpng')