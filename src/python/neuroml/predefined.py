import neuroml.morphology as morphology
from neuroml.morphology import MorphologyArray
import random

def __grand(sigma):
    import random

    random_number=abs(random.gauss(1.0,sigma))
    return random_number

def __branch_decision(probability):
    """
    For a fixed probability returns a 1 or a 0

    The function is used to decide whether a bifibrication should occur
    """        
    return random.random() < probability

def __rall_power(parent_diam,e=1.5):
    """
    Returns the diameter of a child section of a branch 
    according to Rall's Power Law as described
    in Van Ooyen et al 2010. Assumes child branches
    will be of equal diameter.
    """

    child_diam=parent_diam/(2**(1/e))
    return child_diam

def soma(radius=30,length=30):
    section=morphology.Section(radius=radius,length=30)
    return section.morphology


def arborization(bifurcations=3.0,root_L=100.0,term_L=1.0,
                 root_d=10.0,term_d=1,L_sigma=0.0,branch_prob=1.0):

    """
    returns a morphology corresponding to a dendritic tree
    """

    root_section_length=root_L*__grand(L_sigma)
    root_section=morphology.Section(radius=root_d,
                                length=root_section_length)
        
    heads=[root_section]                            
    i=0
    while i<bifurcations:
        i+=1
        new_heads=[]
        for head in heads:
            #make decision whether to branch
            if __branch_decision(branch_prob):
                section_length=(term_L-root_L)*i/bifurcations+root_L
                section_diam=__rall_power(head.radius)
                if section_diam<term_d:
                    section_diam=term_d

                #make two sections for it:
                branch1_l=section_length*__grand(L_sigma)
                branch2_l=section_length*__grand(L_sigma)

                branch1=morphology.Section(length=branch1_l,radius=
                                            section_diam)
                branch2=morphology.Section(length=branch2_l,radius=
                                            section_diam)

                branch1.connect(head)
                branch2.connect(head)
                new_heads+=[branch1,branch2]
                
        heads=new_heads
    
    return root_section.morphology
