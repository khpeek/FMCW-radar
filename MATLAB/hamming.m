function w=hamming(L,varargin)
N=L-1;
n=0:N;
w=0.54-0.46*cos(2*pi*n/N);

if nargin>1
    if strcmp(varargin{1},'periodic')==1
        N=L;
        n=0:N;
        w=0.54-0.46*cos(2*pi*n/N);
        w=w(1:end-1);
    end
end

w=w(:);