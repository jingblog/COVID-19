function dy=SEIR(~,x,A)
SUM = sum(x);
beta=A(1);
theta=A(2);
omiga=A(3);
alpha=A(4);
gamma=A(5);
b=0.0067;
d=0.0074;
dy=[b*SUM-beta*x(1)*x(3)/SUM-d*x(1)+theta*x(4);
    beta*x(1)*x(3)/SUM-d*x(2)-omiga*x(2);
    omiga*x(2) - d*x(3)-alpha*x(3)-gamma*x(3); 
    gamma*x(3)-d*x(4)-theta*x(4)];
end