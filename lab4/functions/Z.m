function Z = Z(R,omega,C,L)
    Z = 1/( sqrt( 1/(R^2) + (omega*C - 1/(omega*L) )^2 ) );
end