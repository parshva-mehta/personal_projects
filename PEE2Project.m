clear
syms s L1 C1 Vin R Va

eqn = (Va - Vin)/(s*L1) + (Va)/(1/(s*C1)) + (Va)/(R) == 0;
LowPass = solve(eqn, Va);

clear
syms s L4 C4 Vin R Va

eqn = (Va - Vin)/(1/(s*C4)) + (Va)/(s*L4) + (Va)/(R) == 0;
HighPass = solve(eqn, Va);

clear
syms s L2 L3 C2 C3 Vin R Va Vb

eqn1 = (Va-Vin)/(1/(s*C2)) + Va/(s*L2) + (Va-Vb)/(s*L3) == 0;
eqn2 = (Vb-Va)/(s*L3) + Vb/(1/(s*C3)) + Vb/R == 0;
 
sol = solve([eqn1, eqn2], [Va,Vb]);
Va = sol.Va;
Midrange = sol.Vb;
%%
clear
LowerFreq = 250;
UpperFreq = 5000;

% Convert to rad/s
UpperFreq = UpperFreq * 2 * pi;
LowerFreq = LowerFreq * 2 * pi;
R = 8;

% Low pass
C1 = 1/(2*R*LowerFreq);
L1 = 1/(LowerFreq^2 * C1);

% High Pass
C4 = 1/(2*R*UpperFreq);
L4 = 1/(UpperFreq^2 * C4);

%% 
C2 = C1;
L2 = L1;
C3 = C4;
L3 = L4; 

syms s
%Low pass
H_sL = (R)/(C1*L1*R*s^2 + L1*s + R);
HL = tf([0 R],[C1*L1*R L1 R]);

%High pass
H_sH = (C1*L1*R*s^2)/(C4*L4*R*s^2 + L4*s + R);
HH = tf([C4*L4*R 0 0],[C4*L4*R L4 R]);

%Bandpass
H_sBP = (C2*L2*R*s^2)/(R + L2*s + L3*s + C2*L2*L3*s^3 + C2*L2*R*s^2 + C3*L2*R*s^2 + C3*L3*R*s^2 + C2*C3*L2*L3*R*s^4);
HBP = tf([0 0 C2*L2*R 0 0], [C2*C3*L2*L3*R C2*L2*L3 (C3*L3*R)+(C3*L2*R)+(C2*L2*R) (L2+L3) R]);

bode(HL, {60,600000})
bode(HH, {60,600000})
bode(HBP,{60,600000})
