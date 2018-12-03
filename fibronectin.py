#!/usr/bin/env python3

import math
from system import make_system
from topology import write_topology_file
from settings import write_lammps_file

class Fibronectins:

    def __init__(self):

        self.side_lengthx = self.side_lengthy = self.side_lengthz = 200

        self.no_rods = 9
        self.beads_per_rod = 10
        self.beads_per_loop = 9
        self.bead_spacing = 1
        self.hydrogen_bond_strength = 1.2;

        self.atoms = []
        self.molecules = []
        self.bonds = []
        self.atomic_index = 0
        self.molecular_index = 0

        self.trajectory_file = "fibro.xyz"



        make_system(self)

        write_topology_file(self)
        write_lammps_file(self)


    def make_monomer(self,x,y,z):


        for i in range(self.no_rods):

            bead_type = 2 if i % 2 == 1 else 3
            self.molecular_index += 1

            for j in range(self.beads_per_rod):

                self.atomic_index += 1

                self.atoms.append((self.atomic_index,self.molecular_index,1,x,y+i*0.5*self.no_rods,z+j*self.bead_spacing))
                self.atoms.append((self.atomic_index+self.beads_per_rod,self.molecular_index,bead_type,x,y+0.15+i*0.5*self.no_rods-1,z+j*self.bead_spacing))

                if j != self.beads_per_rod - 1 :
                    self.bonds.append((self.atomic_index,self.atomic_index+1))
                self.bonds.append((self.atomic_index,self.atomic_index+self.beads_per_rod))



            self.atomic_index += self.beads_per_rod

            for k in range(self.beads_per_loop):

                self.atomic_index += 1
                orientation = 0
                if i % 2 == 0:
                    orientation = 1
                else:
                    orientation = -1
                theta = math.pi/(self.beads_per_loop-1)

                if orientation == 1:


                    self.atoms.append((self.atomic_index, self.molecular_index, 4, x, y+i*0.5*self.no_rods - 2*self.bead_spacing*(1-math.cos(k*theta)),-1+z-2*self.bead_spacing*math.sin(k*theta)))
                    if k == 0:
                        self.bonds.append((self.atomic_index,self.atomic_index-2*self.beads_per_rod))

                    elif k < self.beads_per_loop - 1:
                        self.bonds.append((self.atomic_index,self.atomic_index-1))

                    else:
                        self.bonds.append((self.atomic_index,self.atomic_index-1))
                        if i != 0:
                            print((self.atomic_index,self.atomic_index-4*self.beads_per_rod-self.beads_per_loop-k))
                            self.bonds.append((self.atomic_index,self.atomic_index-4*self.beads_per_rod-self.beads_per_loop-k))

                else:

                    self.atoms.append((self.atomic_index, self.molecular_index, 5, x, y+i*0.5*self.no_rods - 2*self.bead_spacing*(1-math.cos(k*theta)), 1+z+2*self.bead_spacing*math.sin(k*theta)+self.beads_per_rod*self.bead_spacing))

                    if k == 0:
                        print((self.atomic_index,self.atomic_index-self.beads_per_rod-1))
                        self.bonds.append((self.atomic_index,self.atomic_index-self.beads_per_rod-1))

                    elif k < self.beads_per_loop - 1:
                        self.bonds.append((self.atomic_index,self.atomic_index-1))

                    else:
                        print((self.atomic_index,self.atomic_index-1),(self.atomic_index,self.atomic_index-4*self.beads_per_rod))
                        self.bonds.append((self.atomic_index,self.atomic_index-1))
                        self.bonds.append((self.atomic_index,self.atomic_index-4*self.beads_per_rod-k))


if __name__ == "__main__":
    fibronectins = Fibronectins()
