## <font color="powderblue" >Secure Inner Product Computation ⌨</font>

### <font color ="Pink">Algorithm in NuteShell 📔: </font>
A set of encrypted documents, each with two encrypted vocabulary vectors $d', d''$ that states which vocabulary exsists in this document, stored on a server such as a cloud provider. We will be able to do a multi keyword search using two encrypted vocabulary vectors  $q', q''$  on the server and return the matched result without exposing any information to a server about the document neither the query.

<h4><font type ="italic" color ="Green">Code Author: Mahmoud Srewa  </font>👨 , PhD student at the University of Alabama 🏛 - Alsharif labs</h4>

<h4>Refrence Paper</h4> <a href="https://ieeexplore.ieee.org/document/6674958">Privacy-Preserving Multi-Keyword Ranked Search over Encrypted Cloud Data</a> 

 <h3><font color = "orange "> *__Steps in Nutshell__* 🍜: </font></h3>

### <u> First the owner should perform some operations on the documents. </u>



1. Create a vocabulary vector of size $n$ that will be used to index the documents.



2. For each document $d_i \; in \; \{d_1,d_2, \dots, d_k\}$, create a simple vocabulary vector $\vec{p_i}$ index.



3. generate two $n*n$-dimensional random secret key matrices $m_1, m_2$.



4. generate a random vector matrix $S$ of size $n$ which is used as a splitting factor



5. Create two random vectors of size $n$ , $\vec{p'_i}$ and $\vec{p''_i}$, which will be used to split the plain index into them.



6. The following is how the splitting phase was completed:



For each document $i$, check if value of $s$ at specific index $i$ equal the following<br>



- If $s[i] = 0$, the two split index values at $i$ are equal to the plain index value at $i$.



- If $s[i]=1$, we check the plain index value at $i$.

    - If plainIndex $[i] == 1$, then generate two random numbers with sums of $1$ for both split indexes.
    - If plainIndex $[i] == 0$, then generate two random numbers with sums of zero for both split indexes.


7. now encryption phase of two split indexes before sending them to the server, as the following
$$ \{M_1\cdot\vec{p'_i},M_2\cdot\vec{p''_i}\} $$


8. Finally for each document encrypt it using proper algorithm along with it's encrypted vocabulary index


### <u>Second the User procedure to generate query index</u>



1. Use a vocabulary vector of size $n$ same as the one with the owner that will be used to index the query.



2. For a query generate a simple vocabulary vector $\vec{q}$ index that corresponds to keywords you are looking for.



3. Recvice from the owner  two $n*n$-dimensional random secret key matrices which is $m_1^{-1}, m_2^{-1}$.



4. Recvice from the owner vector matrix $S$ of size $n$ which is used as a splitting factor



5. Create two random vectors of size $n$, $\vec{q'_i}$ and $\vec{q''_i}$, which will be used to split the plain index into them.


6. For query index, check if the value of $s$ at specific index $i$ equal the following<br>



- If $s[i] = 1$, the two split index values at $i$ are equal to the plain index value at $i$.



- If $s[i]=0$, we check the plain index value at $i$.
    - If plainIndex $[i] == 1$, then generate two random numbers with sums of $1$ for both split indexes.
    - If plainIndex $[i] == 0$, then generate two random numbers with sums of zero for both split indexes.


7. now encryption phase of two splited indexes before sending them to the server, as the following
$$ \{M_1^{-1}\cdot\vec{q'} ,M_2^{-1}\cdot\vec{q''}\} $$


8. Finally, send the calculated encrypted query vocabulary index to the server.



### <u>Third the Server operation to calculate the result of a query</u>


1. The server receives the encrypted documents $d_i \; in\; \{d_1,d_2 \dots d_k\}$ where k is the total number of documents


2. also received two encrypted vocabulary index for each document


3. Whenever the user wants to make a query against the documents, he sends the encrypted query index to server.


4. The server performs a dot product on the documents index and the query index sorts them by desc, and returns them to the user.


5. The dot product count is how many keywords found in the document index that is requested by a user


6. the server do the dot product without knowing any information about the query neither the server


$$ \{M_1\cdot\vec{p'_i} , M_2\cdot\vec{p''_i}\}  \cdot \{M_1^{-1}\cdot\vec{q'}, M_2^{-1}\cdot\vec{q''}\}$$
$$ \because  M_1 \cdot M_1^{-1}  = I$$
$$\therefore \vec{p'_i} \cdot \vec{q'_i} + \vec{p''_i} \cdot \vec{q''} $$
$$\because both\:index\:splited\:on\:same\:splitting\:vector\: \vec{S}$$
$$\therefore \vec{D_i} \cdot \vec{Q_i}$$


<center> The result is a dot product of the document's vocabulary index and the query's vocabulary index, which is a similarity calculation.


