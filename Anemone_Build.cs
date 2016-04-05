/// <copyright file="Anemone_Build.cs">
/// MIT License
///
/// Copyright(c) 2016 Erik Høyrup Jørgensen
///
/// Permission is hereby granted, free of charge, to any person obtaining a copy
/// of this software and associated documentation files (the "Software"), to deal
/// in the Software without restriction, including without limitation the rights
/// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
/// copies of the Software, and to permit persons to whom the Software is
/// furnished to do so, subject to the following conditions:
///
/// The above copyright notice and this permission notice shall be included in all
/// copies or substantial portions of the Software.
///
/// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
/// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
/// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
/// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
/// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
/// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
/// SOFTWARE.
/// </copyright>
/// <author>Erik Høyrup Jørgensen</author>
/// <date>03/25/2016 18:15</date>
/// <summary>Class for build methods required by Unity for the Anemone project.</summary>

using System.Collections.Generic;
using System.Text;

using UnityEngine;
using UnityEditor;



// Copy this to your [project]/Assets/Editor folder


/// <summary>
/// Part of the Anemone CI (https://github.com/winnak/anemone)
/// </summary>
namespace Anemone
{
    /// <summary>
    /// Contains all methods required by the build slaves of Anemone
    /// </summary>
    internal static class Build
    {
        private const string kDefaultBuildPath = "./buildstmp/"; // has to be a unix file path

        /// <summary>
        /// Builds a debug build for windows to the <see cref="kDefaultBuildPath"/>
        /// </summary>
        [MenuItem("File/Anemone Build/Windows x86 (Debug)")]
        private static void WindowsDebug()
        {
            StringBuilder path = new StringBuilder();
            path.Append(kDefaultBuildPath);
            path.Append(Application.productName);
            path.Append("x86.exe");

            if (BuildPipeline.isBuildingPlayer)
            {
                Debug.LogError("BUILD FAILED: Unity is already building the project");
                return;
            }

            Debug.Log("Retrieving scenes:");
            List<string> levels = GetScenes();

            Debug.Log("Unity building");
            string errorMessage = BuildPipeline.BuildPlayer(
                levels.ToArray(),
                path.ToString(),
                BuildTarget.StandaloneWindows,
                (BuildOptions.AllowDebugging | BuildOptions.Development));

            if (!string.IsNullOrEmpty(errorMessage))
            {
                Debug.LogError(errorMessage);
            }

            Debug.Log("Finished");
        }

        /// <summary>
        /// Builds a windows build to the <see cref="kDefaultBuildPath"/>
        /// </summary>
        [MenuItem("File/Anemone Build/Windows x86")]
        private static void Windows()
        {
            StringBuilder path = new StringBuilder();
            path.Append(kDefaultBuildPath);
            path.Append(Application.productName);
            path.Append("x86.exe");

            if (BuildPipeline.isBuildingPlayer)
            {
                Debug.LogError("BUILD FAILED: Unity is already building the project");
                return;
            }

            Debug.Log("Retrieving scenes:");
            List<string> levels = GetScenes();

            Debug.Log("Unity building");
            string errorMessage = BuildPipeline.BuildPlayer(
                levels.ToArray(),
                path.ToString(),
                BuildTarget.StandaloneWindows,
                BuildOptions.None);

            if (!string.IsNullOrEmpty(errorMessage))
            {
                Debug.LogError(errorMessage);
            }

            Debug.Log("Finished");
        }

        /// <summary>
        /// Fetches all scenes in the <see cref="EditorBuildSettings"/> and prints out which goes in and which does not.
        /// </summary>
        /// <returns>A list of active scenes.</returns>
        private static List<string> GetScenes()
        {
            List<string> levels = new List<string>();
            List<string> notadded = new List<string>();

            for (int i = 0; i < EditorBuildSettings.scenes.Length; i++)
            {
                string scenePath = EditorBuildSettings.scenes[i].path;
                if (EditorBuildSettings.scenes[i].enabled)
                {
                    levels.Add(scenePath);
                    Debug.Log(scenePath);
                }
                else
                {
                    notadded.Add(scenePath);
                }
            }

            if (notadded.Count > 0)
            {
                Debug.Log("Following scenes were not added:");
                foreach (var scene in notadded)
                {
                    Debug.Log(scene);
                }
            }

            return levels;
        }
    }
}
