from __future__ import absolute_import
from builtins import str
import unittest
import sys, os, re
import forcebalance.molecule
from __init__ import ForceBalanceTestCase
import numpy as np

class TestPDBMolecule(ForceBalanceTestCase):
    def __init__(self, methodName='runTest'):
        super(TestPDBMolecule,self).__init__(methodName)
        self.source = 'dms_conf.pdb'

    def setUp(self):
        super(TestPDBMolecule,self).setUp()
        os.chdir('test/files')
        try: self.molecule = forcebalance.molecule.Molecule(self.source, build_topology=False)
        except IOError:
            self.skipTest("Input pdb file test/files/%s doesn't exist" % self.source)
        except:
            self.fail("\nUnable to open pdb file")

    def tearDown(self):
        os.system('rm -rf {name}.xyz {name}.gro {name}.arc'.format(name=self.source[:-4]))
        super(TestPDBMolecule,self).tearDown()

    def test_xyz_conversion(self):
        """Check molecule conversion from pdb to xyz format"""
        self.logger.debug("\nCreating xyz file from pdb... ")
        self.molecule.write(self.source[:-3] + 'xyz')
        self.logger.debug("done\nTrying to read generated xyz file... ")
        try:
            molecule1 = forcebalance.molecule.Molecule(self.source[:-3] + 'xyz', build_topology=False)
            self.logger.debug("ok\n")
        except:
            self.fail("\nConversion to xyz format creates unreadable file")

        self.logger.debug("Checking that conversion has not changed molecule spatial coordinates\n")
        self.assertEqual(self.molecule.Data['xyzs'][0],molecule1.Data['xyzs'][0],
        msg = "\nConversion from pdb to xyz yields different xyz coordinates\npdb:\n%s\n\ngro:\n%s\n" %\
        (str(self.molecule.Data['xyzs'][0]), str(molecule1.Data['xyzs'][0])))

    def test_measure_distances(self):
        """Check measure distance functions"""
        result = np.array(self.molecule.measure_distances(1701, 1706))
        EXPECTED_DISTANCE_RESULTS = np.array([1.80])
        self.assertNdArrayEqual(EXPECTED_DISTANCE_RESULTS,result,delta=0.01,
                                msg="\nMeasured distance has changed from previously calculated values.\n"
                                "If this seems reasonable, update EXPECTED_DISTANCE_RESULTS in test_molecule.py with these values")

    def test_measure_angles(self):
        """Check measure angle functions"""
        result = np.array(self.molecule.measure_angles(1771, 1769, 1772))
        EXPECTED_ANGLE_RESULTS = np.array([114.11])
        self.assertNdArrayEqual(EXPECTED_ANGLE_RESULTS,result,delta=0.01,
                                msg="\nMeasured angle has changed from previously calculated values.\n"
                                "If this seems reasonable, update EXPECTED_ANGLE_RESULTS in test_molecule.py with these values")

    def test_measure_dihedrals(self):
        """Check measure dihedral functions"""
        result = np.array(self.molecule.measure_dihedrals(1709, 1706, 1701, 1702))
        EXPECTED_DIHEDRAL_RESULTS = np.array([176.54])
        self.assertNdArrayEqual(EXPECTED_DIHEDRAL_RESULTS,result,delta=0.01,
                                msg="\nMeasured dihedral angle has changed from previously calculated values.\n"
                                "If this seems reasonable, update EXPECTED_DIHEDRAL_RESULTS in test_molecule.py with these values")

    def test_gro_conversion(self):
        """Check molecule conversion from pdb to gro format"""
        self.logger.debug("\nCreating gro file from pdb... ")
        self.molecule.write(self.source[:-3] + 'gro')
        self.logger.debug("done\nTrying to read generated gro file... ")
        try:
            molecule1 = forcebalance.molecule.Molecule(self.source[:-3] + 'gro', build_topology=False)
            self.logger.debug("ok\n")
        except:
            self.fail("\nConversion to gro format creates unreadable file")

        self.logger.debug("\nChecking that conversion has not changed number of residues\n")
        self.assertEqual(len(self.molecule.Data['resid']), len(molecule1.Data['resid']),
                        msg = "\nConversion from pdb to gro yields different number of residues")

        self.logger.debug("Checking that conversion has not changed molecule spatial coordinates\n")
        self.assertEqual(self.molecule.Data['xyzs'][0],molecule1.Data['xyzs'][0],
        msg = "\nConversion from pdb to gro yields different xyz coordinates\npdb:\n%s\n\ngro:\n%s\n" %\
        (str(self.molecule.Data['xyzs'][0]), str(molecule1.Data['xyzs'][0])))

    def test_arc_conversion(self):
        """Check molecule conversion from pdb to arc format"""
        self.logger.debug("\nCreating arc file from pdb... ")
        self.molecule.Data['tinkersuf']=['']*len(self.molecule.Data['resname'])  # suppress topology warning
        self.molecule.write(self.source[:-3] + 'arc')
        self.logger.debug("done\nTrying to read generated gro file... ")
        try:
            molecule1 = forcebalance.molecule.Molecule(self.source[:-3] + 'arc',build_topology=False)
            self.logger.debug("ok\n")
        except:
            self.fail("\nConversion to arc (TINKER) format creates unreadable file")

        self.logger.debug("Checking that conversion has not changed molecule spatial coordinates\n")
        self.assertEqual(len(self.molecule.Data['resid']), len(molecule1.Data['resid']),
                        msg = "\nConversion from pdb to arc (TINKER) yields different number of residues")


        self.assertEqual(self.molecule.Data['xyzs'][0],molecule1.Data['xyzs'][0],
        msg = "\nConversion from pdb to arc yields different xyz coordinates\npdb:\n%s\n\narc:\n%s\n" %\
        (str(self.molecule.Data['xyzs'][0]), str(molecule1.Data['xyzs'][0])))

    def test_pdb_topology_build(self):
        """Check reading pdb with build_topology=True"""
        self.logger.debug("\nTrying to read molecule with topology... ")
        try:
            molecule = forcebalance.molecule.Molecule(self.source, build_topology=True)
            self.logger.debug("done\nChecking molecule has correct number of residues\n")
        except:
            self.fail("\nFailed to load pdb with build_topology=True")

        self.assertEqual(len(self.molecule.Data['resid']), len(molecule.Data['resid']),
                        msg = "\nTopology build yields different number of residues")

class TestLipidGRO(ForceBalanceTestCase):
    def __init__(self, methodName='runTest'):
        super(TestLipidGRO,self).__init__(methodName)
        self.source = 'lipid.gro'

    def setUp(self):
        super(TestLipidGRO,self).setUp()
        os.chdir('test/files')
        try: self.molecule = forcebalance.molecule.Molecule(self.source, toppbc=True)
        except IOError:
            self.skipTest("Input pdb file test/files/%s doesn't exist" % self.source)
        except:
            self.fail("\nUnable to open gro file")
            
    def test_measure_dihedrals(self):
        """Check measure dihedral functions"""
        result = np.array(self.molecule.measure_dihedrals(1131, 1112, 1113, 1114))
        EXPECTED_DIHEDRAL_RESULTS = np.array([-157.223])
        self.assertNdArrayEqual(EXPECTED_DIHEDRAL_RESULTS,result,delta=0.001,
                                msg="\nMeasured dihedral angle has changed from previously calculated values.\n"
                                "If this seems reasonable, update EXPECTED_DIHEDRAL_RESULTS in test_molecule.py with these values")

    def test_lipid_molecules(self):
        """Check for the correct number of molecules in a rectangular cell with broken molecules"""
        self.logger.debug("\nTrying to read lipid conformation... ")
        self.assertEqual(len(self.molecule.molecules), 3783, msg = "\nIncorrect number of molecules for lipid structure")

class TestWaterPDB(ForceBalanceTestCase):
    def __init__(self, methodName='runTest'):
        super(TestWaterPDB,self).__init__(methodName)
        self.source = 'waterbox500.pdb'

    def setUp(self):
        super(TestWaterPDB,self).setUp()
        os.chdir('test/files')
        try: self.molecule = forcebalance.molecule.Molecule(self.source, toppbc=True)
        except IOError:
            self.skipTest("Input pdb file test/files/%s doesn't exist" % self.source)
        except:
            self.fail("\nUnable to open pdb file")

    def test_water_molecules(self):
        """Check for the correct number of molecules in a cubic water box"""
        self.logger.debug("\nTrying to read water conformation... ")
        self.assertEqual(len(self.molecule.molecules), 500, msg = "\nIncorrect number of molecules for water structure")

class TestAlaGRO(ForceBalanceTestCase):
    def __init__(self, methodName='runTest'):
        super(TestAlaGRO,self).__init__(methodName)
        self.source = 'ala.gro'

    def setUp(self):
        super(TestAlaGRO,self).setUp()
        os.chdir('test/files')
        try: self.molecule = forcebalance.molecule.Molecule(self.source)
        except IOError:
            self.skipTest("Input gro file test/files/%s doesn't exist" % self.source)
        except:
            self.fail("\nUnable to open gro file")

    def test_ala_molecules(self):
        """Check for the correct number of bonds in a simple molecule"""
        self.logger.debug("\nTrying to read alanine dipeptide conformation... ")
        self.assertEqual(len(self.molecule.bonds), 21, msg = "\nIncorrect number of bonds for alanine dipeptide structure")

class TestGalbPNPMol2(ForceBalanceTestCase):
    def __init__(self, methodName='runTest'):
        super(TestGalbPNPMol2,self).__init__(methodName)
        self.source = 'pNP-0LB-tleap.mol2'

    def setUp(self):
        super(TestGalbPNPMol2,self).setUp()
        os.chdir('test/files')
        try: self.molecule = forcebalance.molecule.Molecule(self.source)
        except IOError:
            self.skipTest("Input gro file test/files/%s doesn't exist" % self.source)
        except:
            self.fail("\nUnable to open mol2 file")

    def test_read_galb(self):
        """Check for the correct number of bonds in a simple molecule"""
        self.logger.debug("\nTrying to read alanine dipeptide conformation... ")
        #self.logger.info("%s\n" % str(self.molecule.resname))
        self.assertEqual(self.molecule.resname, 14*['PNP']+22*['0LB'], msg="\nIncorrect residue names")
        self.assertEqual(self.molecule.elem, ['O', 'N', 'O', 'C', 'C', 'C', 'H', 'H', 'C', 'H', 'C', 'H', 'C', 'O', 'C', 'H', 'O', 'C', 'H', 'C', 'H', 'H', 'O', 'H', 'C', 'H', 'O', 'H', 'C', 'H', 'O', 'H', 'C', 'H', 'O', 'H'], msg="\nIncorrect atomic symbols")
        self.assertEqual(len(self.molecule.bonds), 37, msg="\nIncorrect number of bonds for pNP-0LB structure")

if __name__ == '__main__':
    unittest.main()
