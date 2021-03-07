import numpy as np

################################################################################
#                               POINT DISTANCES                                #
################################################################################

##########################################################################
# Method to determine the distance of a set of points P2_k to a point P1 #
##########################################################################
def distancePointsPoint(P1,P2):
    """Calculate the distance between a set of points P2_k and a point P1. """
    return np.atleast_2d(P2-P1)


################################################################################
# Method to determine the distance of a set of line segments L_k to a point P1 #
################################################################################
def distanceLinesPoint(P,A,AB):
    """Calculate the distance between a set of line segments L_k and a point P.
    The line segments L_k are defined by points A_k and directors AB_k, so that:

                L_k = A_k+t_k*AB_k  with  t_k in [0,1].

    To ensure correct results for finite lines, the parameter t has to be
    calculated at first. Afterwards, different cases can be distinguished for
    which the calculation is reduced to the problem of the distance of points.
    """

    # get required vectors:
    PA = np.atleast_2d(A-P)                                                     # vectors P->A_k

    # get parameters t for minimum distance of point and line
    t = -np.sum(PA*AB,axis=1)/np.sum(AB*AB,axis=1)                              # projection of AP in AB direction
    t=_constrainParameter(t)                                                    # fix parameter t to closest segment points, if outside [0,1]

    # calculate distance vectors
    distVec = PA+AB*np.atleast_2d(t).T

    # return distance vectors and parameters
    return distVec, t


########################################################################
# Method to determine the distance of a set of planes E_k to a point P #
########################################################################
def distancePlanesPoint(P,Q0,R1,R2):
    """Calculate the distance between a set of planes E_k and a point P.
    The planes E_k are defined by their origins Q0_k and their end points Q1_k
    and Q2_k, so that:

        E_k = Q0_k+u_k*R1_k+v_k*R2_k  with  u_k, v_k in [0,1].

    To ensure correct results for finite plane surfaces, the parameters u_k and
    v_k are calculated at first. They can be determined by using the projection
    P' of P onto the plane. All calculations are only valid for perpendicular
    directors R1_k=(Q1_k-Q0_k) and R2_k=(Q2_k-Q0_k).
    """

    # get required vectors:
    QP = np.atleast_2d(P-Q0)                                                    # distance vectors of plane origins and P

    # get parameters u_k and v_k for minimum distance of point and (infinite) plane
    u = np.sum(QP*R1,axis=1)/np.sum(R1*R1,axis=1)                               # parameters u_k
    v = np.sum(QP*R2,axis=1)/np.sum(R2*R2,axis=1)                               # parameters v_k

    # apply constraints
    u=_constrainParameter(u)                                                    # apply constraints for u_k
    v=_constrainParameter(v)                                                    # apply constraints for v_k

    # calculate distance vectors
    distVec = -QP+R1*np.atleast_2d(u).T+R2*np.atleast_2d(v).T

    # return distance vectors and parameters
    return distVec, u, v



################################################################################
#                               LINE DISTANCES                                 #
################################################################################

#################################################################################
# Method to determine the distance of a set of points P_k to a line segment L_k #
#################################################################################
def distancePointsLine(A,AB,P):
    """Calculate the distance between a set of points P_k and a line segment L.
    The line segment L is defined by point A and director AB, so that:

                L = A+t*AB  with  t in [0,1].

    To ensure correct results for finite lines, the parameter t has to be
    calculated at first. Afterwards, different cases can be distinguished for
    which the calculation is reduced to the problem of the distance of points.
    """

    # get required vectors:
    AP = np.atleast_2d(P-A)                                                     # vectors A->P_k

    # get parameters t for minimum distance of point and line
    t = np.sum(AP*AB,axis=1)/np.sum(AB*AB,axis=1)                               # projection of AP in AB direction
    t=_constrainParameter(t)                                                    # constrain parameter t to closest segment points, if outside [0,1]

    # calculate distance vectors
    distVec = AP-AB*np.atleast_2d(t).T

    # return distance vectors and parameters
    return distVec, t


########################################################################################
# Method to determine the distance of a set of line segments L2_k to a line segment L1 #
########################################################################################
def distanceLinesLine(A,AB,C,CD,rtol=1e-8):
    """Calculate the distance between a set of line segments L2_k and a line
    segment L1. L1 and is defined by starting point A and director AB while
    L2_k are defined by starting points C_k and directors CD_k, so that:

            L1 = A + t*AB          with  t in [0,1]     ,
            L2_k = C_k + u_k*CD_k  with  u_k in [0,1]   .

    To ensure a robust implementation, the algorithm described in "On Fast
    Computation Of Distance Between Line Segments" (Lumelsky, 1985), is
    implemented. It is based on the determination of the parameters t and u_k
    and handles parallel lines as a special case. Degenerate lines, i.e. points,
    are only handled for L2_k here. This is done, because the distance of a line
    L1 to a set of planes E_k can be reformulated as the distance of this line
    to its projections onto the planes. These projections can be points, if the
    original line L1 is perpendicular to the plane. However, at least for L1 it
    has to be ensured that it is a "real" line.
    """

    # get required distance vectors
    AC = np.atleast_2d(C-A)                                                     # distance of starting points A and C_k

    # get required quantities for distance minimization
    a = np.sum(AB*AB,axis=1)                                                    # squared length of L1 (a>0, since degenerate segments are not allowed)
    b = np.sum(AB*CD,axis=1)                                                    # scalar products of directors of L1 and L2_k
    c = np.sum(CD*CD,axis=1)                                                    # squared length of L2_k (c>=0, since degenerate segments are allowed)
    d = np.sum(AC*AB,axis=1)                                                    # scalar product of director of L1 with distance of starting points
    e = np.sum(AC*CD,axis=1)                                                    # scalar product of director of L2_k with distance of starting points
    cross = a*c-b*b                                                             # squared length of cross product of directors of L1 and L2_k (cross >= 0)

    # determine effective tolerance to detect degenerate lines
    # To see if one of the lines L2_k is degenerate, i.e. a point, it has to be
    # compared to L1 -> scale rtol with squared length a of L1
    tolD=rtol*a                                                                 # tolerance to identify degenerate lines

    # determine effective tolerance to detect parallel lines
    # To see if the binormal vector is almost 0, it has to be compared to the
    # the extends of the vectors under consideration -> scale rtol with squared
    # length of the smaller segment for each pair
    tolP=rtol*np.minimum(a,c)                                                   # tolerance to identify parallel lines

    # find degenerate lines
    # Degenerate lines are handled different from "normal" lines, since no
    # iteration - to find the parameter u_k - is needed. Here, the indices of
    # all degenerate lines are determined
    indD = c<=tolD                                                              # indices of degenerate lines
    indL = ~indD                                                                # indices of actual lines

    # find parallel lines
    # Among all lines that are not degenereate, the parallel ones have to be
    # found, since the algorithm starts by setting t=0 for them.
    indP = np.logical_and(cross<=tolP, indL)                                    # indices of parallel line segments
    indN = np.logical_and(~indP, indL)                                          # indices of remaining, "normal" lines

    # Lumelsky algorithm to determine t and u for the minimum distance
    # (1) determine initial t
    t = c*d-b*e                                                                 # initialize t by calculating its nominator
    t[indN]=t[indN]/cross[indN]                                                 # determine actual value of t for all "normal" lines
    t[indP]=0                                                                   # set t=0 for all parallel lines
    t=_constrainParameter(t)                                                    # fix t where it is out of the parameter range (apply constraint t in [0,1])
    # (2) determine u_k
    u = b*t-e                                                                   # initialize u_k by calculating its nominator
    u[indL]=u[indL]/c[indL]                                                     # determine actual value of u for all "non-degenerate" lines (parallel lines included)
    u[indD]=-1                                                                  # set u_k=-1 for all degenerate lines -> this leads to a constraint u_k=0 and automatically triggers a recalculation of t
    indR = np.logical_or(u<0,u>1)                                               # determine indices of distances, for which t has to be recalculated, since the initial guess did not yield a minumum for u_k
    u=_constrainParameter(u)                                                    # fix u_k where they are out of the parameter range
    # (3) recalculate t where needed
    t[indR] = (b[indR]*u[indR]+d[indR])/a                                       # recalculate t, where required
    t[indR]=_constrainParameter(t[indR])                                        # fix t, where it was recalculated

    # (4) determine distance vectors
    distVec = AC+CD*np.atleast_2d(u).T-AB*np.atleast_2d(t).T

    # return distance vectors and parameters
    return distVec, t, u


#################################################################################
# Method to determine the distance of a set of planes E_k to a line segment L_k #
#################################################################################
def distancePlanesLine(A,AB,Q0,R1,R2,rtol=1e-8):
    """Calculate the distance between a set of planes E_k and a line segment L.
    L is defined by its start point A and director AB, while the planes E_k are
    defined by their origins Q0_k and their directors R1_k and R2_k, so that:

        L = A+t*AB                    with  t in [0,1]         ,
        E_k = Q0_k+u_k*R1_k+v_k*R2_k  with  u_k, v_k in [0,1]  .

    To ensure correct results for finite plane surfaces, the parameters t, u_k
    and v_k are calculated at first. They are determined by using the projection
    L' of L onto the plane. This allows to reformulate the problem to the one of
    the distance of line segments. All calculations are valid for perpendicular
    directors R1_k=(Q1_k-Q0_k) and R2_k=(Q2_k-Q0_k).
    """

    # get required vectors
    QA = np.atleast_2d(A-Q0)                                                    # distance vectors of plane origin and line point A
    QB = np.atleast_2d(QA+AB)                                                   # distance vectors of plane origin and line point B

    # (1) project line L onto the plane - account for constraints
    # get parameters uA, vA and uB, vB for projections of A and B onto the planes (see distancePlanesPoint)
    uA = _constrainParameter(np.sum(QA*R1,axis=1)/np.sum(R1*R1,axis=1))         # determine u_k for projection of Point A onto the constrained planes E_k
    uB = _constrainParameter(np.sum(QB*R1,axis=1)/np.sum(R1*R1,axis=1))         # determine u_k for projection of Point B onto the constrained planes E_k
    vA = _constrainParameter(np.sum(QA*R2,axis=1)/np.sum(R2*R2,axis=1))         # determine v_k for projection of Point A onto the constrained planes E_k
    vB = _constrainParameter(np.sum(QB*R2,axis=1)/np.sum(R2*R2,axis=1))         # determine v_k for projection of Point B onto the constrained planes E_k
    Ap = Q0+R1*np.atleast_2d(uA).T+R2*np.atleast_2d(vA).T                       # starting points Ap_k of projected lines Lp_k
    ApBp = Q0+R1*np.atleast_2d(uB-uA).T+R2*np.atleast_2d(vB-vA).T               # directors ApBp_k of projected lines Lp_k

    # (2) use Lumelsky algorithm to determine distances Lp_k to L
    distVec, *parameters = distanceLinesLine(A,AB,Ap,ApBp)

    # (3) determine u and v from parameters p_k of projected lines
    P = Ap-Q0+ApBp*np.atleast_2d(parameters[1]).T
    u = np.sum(P*R1,axis=1)/np.sum(R1*R1,axis=1)
    v = np.sum(P*R2,axis=1)/np.sum(R2*R2,axis=1)

    # return distance vectors and parameters
    return distVec, parameters[0], u, v



################################################################################
#                              PLANE DISTANCES                                 #
################################################################################

#####################################################################
# Method to determine the distance of a set points P_k to a plane E #
#####################################################################
def distancePointsPlane(P,Q0,R1,R2):
    """Calculate the distance between a set of points P_k and a plane E. The
    plane E is defined by its origin Q0 and directors R1 and R2, so that:

        E = Q0+u*R1+v*R2  with  u, v in [0,1].

    To ensure correct results for finite plane surfaces, the parameters u and v
    v are calculated at first. They can be determined by using the projection
    P'_k of P_k onto the plane. All calculations are only valid for perpendicular
    directors R1=(Q1-Q0) and R2=(Q2-Q0).
    """

    # get required vectors:
    QP = np.atleast_2d(P-Q0)                                                    # distance vectors of plane origin and P_k

    # get parameters u and v for minimum distance of unconstrained plane and point
    u = np.sum(QP*R1,axis=1)/np.sum(R1*R1,axis=1)                               # parameters u
    v = np.sum(QP*R2,axis=1)/np.sum(R2*R2,axis=1)                               # parameters v

    # apply constraints
    u=_constrainParameter(u)                                                    # apply constraints for u_k
    v=_constrainParameter(v)                                                    # apply constraints for v_k

    # calculate distance vectors
    distVec = QP-R1*np.atleast_2d(u).T-R2*np.atleast_2d(v).T

    # return distance vectors and parameters
    return distVec, u, v



################################################################################
#                             INTERNAL METHODS                                 #
################################################################################

############################################################
# Internal Method to constrain parameters of line segments #
############################################################
def _constrainParameter(p):
    """This method fixes the parameters of line segments to be equal to the
    values of the closest boundary points, if they are outside the segments
    range [0,1].
    """
    p[p<=0]=0                                                                   # p is smaller than 0 -> assign 0, since point at t=0 is closest point in segment
    p[p>=1]=1                                                                   # p is bigger than 1 -> assign 1, since point at t=1 is closest point in segment

    # return constrained parameters
    return p
